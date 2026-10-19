"""Run with python3 -m unittest -v."""
import tempfile
import unittest
from pathlib import Path
from app import TicketStore

class TicketTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'test.db'
        self.store = TicketStore(self.path)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_persists_after_reopen(self):
        number = self.store.create('Alex', 'Wi-Fi failure', 'High')
        self.store.close()
        self.store = TicketStore(self.path)
        self.assertEqual(self.store.search()[0]['id'], number)

    def test_status_filter_and_counts(self):
        number = self.store.create('Alex', 'Wi-Fi failure', 'High')
        self.assertTrue(self.store.update_status(number, 'Resolved'))
        self.assertEqual(len(self.store.search(status='Open')), 0)
        self.assertEqual(self.store.summary()['Resolved'], 1)
        self.assertFalse(self.store.update_status(999, 'Open'))

    def test_invalid_values(self):
        for values in [('', 'issue', 'Low'), ('Alex', ' ', 'Low'), ('Alex', 'issue', 'Urgent')]:
            with self.assertRaises(ValueError): self.store.create(*values)
        with self.assertRaises(ValueError): self.store.update_status(1, 'Deleted')

    def test_search_is_literal_and_case_insensitive(self):
        self.store.create("O'Brien", 'Wi-Fi issue', 'Low')
        self.assertEqual(len(self.store.search('WI-FI')), 1)
        self.assertEqual(len(self.store.search("O'Brien")), 1)
        self.assertEqual(len(self.store.search("' OR 1=1 --")), 0)
        self.assertEqual(len(self.store.search('%')), 0)

if __name__ == '__main__': unittest.main()
