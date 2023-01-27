import unittest
from atm import ATM
from atm import User
from atm import ChequeAccount
from atm import SavingAccount

class TestATM(unittest.TestCase):

    def test_import(self):
        atm = ATM()
        atm.importData()
        self.assertIsNotNone(atm.users, "Imported users from text file")
        self.assertIsNotNone(atm.accounts, "Imported accounts from text file")
    def test_login(self):
        atm = ATM()
        atm.importData()
        atm.login('004')
        self.assertIsNone(atm.currentUser, "User ID bad login")
        with self.assertRaises(AttributeError):
            atm.login(4)
        atm.login('001')
        self.assertEqual(atm.currentUser.firstname, 'John')
        self.assertEqual(atm.currentUser.surname, 'Smith')
        atm.login('002')
        self.assertEqual(atm.currentUser.firstname, 'Leanne')
        atm.login('NotANumber')
        self.assertIsNone(atm.currentUser)

    def test_selectAccount(self):
        atm = ATM()
        atm.importData()
        atm.login('001')
        atm.selectTransaction('h')
        self.assertIsNone(atm.currentUser)
        self.assertIsNone(atm.currentAccount)
        with input("1"):
            self.assertEqual(atm.selectTransaction("1"), ("1"))


if __name__ == '__main__':

    unittest.main()