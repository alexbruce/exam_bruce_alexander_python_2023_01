import sys
import unittest
from unittest import mock
from src.atm import ATM
from src.atm import User
from src.atm import SavingAccount
sys.path.append('..')

class TestATM(unittest.TestCase):

    def setUp(self):
        self.atm = ATM()
        self.atm.importData()
    def test_import(self):
        self.assertIsNotNone(self.atm.users, "Imported users from text file")
        self.assertIsNotNone(self.atm.accounts, "Imported accounts from text file")
    def test_handleError(self):
        self.atm.error = True
        self.atm.currentUser = User('001','Alex','Bruce','0404040404')
        self.atm.currentAccount = SavingAccount('001','123456','Saving','690','1')
        self.atm.handleError("Test Messsage")
        self.assertTrue(self.atm.error)
        self.assertIsNone(self.atm.currentUser)
        self.assertIsNone(self.atm.currentAccount)

    def test_beginTransaction(self):
        self.assertFalse(self.atm.error)
        self.assertIsNone(self.atm.currentUser)
        self.assertIsNone(self.atm.currentAccount)

    def test_login(self):
        self.atm.login('004')
        self.assertIsNone(self.atm.currentUser)
        with self.assertRaises(AttributeError):
            self.atm.login(4)
        self.atm.login('001')
        self.assertEqual(self.atm.currentUser.firstname, 'John')
        self.assertEqual(self.atm.currentUser.surname, 'Smith')
        self.atm.login('002')
        self.assertEqual(self.atm.currentUser.firstname, 'Leanne')
        self.atm.login('NotANumber')
        self.assertIsNone(self.atm.currentUser)
    @mock.patch('src.atm.input', create=True)
    def test_selectTransaction(self, mockedInput):
        self.atm.login('001')
        self.atm.selectTransaction('h')
        self.assertIsNone(self.atm.currentUser)
        self.assertIsNone(self.atm.currentAccount)

        self.atm.login('001')
        mockedInput.side_effect = ['2', '50']
        self.atm.selectTransaction('1')
        self.assertEqual(self.atm.currentAccount.AccountNumber, "7814135", "Error in select transaction")

        self.atm.login('001')
        mockedInput.side_effect = ['1', '50']
        self.atm.selectTransaction('1')
        self.assertEqual(self.atm.currentAccount.AccountNumber, "9264945", "Error in select transaction")

        self.atm.login('001')
        mockedInput.side_effect = ['3']
        self.atm.selectTransaction('1')
        self.assertIsNone(self.atm.currentUser)
        self.assertIsNone(self.atm.currentAccount)

        self.atm.login('002')
        mockedInput.side_effect = ['1', '50']
        self.atm.selectTransaction('2')
        self.assertEqual(self.atm.currentAccount.OpeningBalance, 1150.00)
    @mock.patch('src.atm.input', create=True)
    def test_handleDeposit(self, mockedInput):
        self.atm.login('001')
        mockedInput.side_effect = ['1', '50']
        self.atm.selectTransaction('1')
        self.assertEqual(self.atm.currentAccount.OpeningBalance, 550.90)

        self.atm.login('001')
        mockedInput.side_effect = ['1', 'h']
        self.atm.selectTransaction('1')
        self.assertIsNone(self.atm.currentAccount)

    @mock.patch('src.atm.input', create=True)
    def test_handleWithdrawal(self, mockedInput):
        self.atm.login('001')
        mockedInput.side_effect = ['1', '50']
        self.atm.selectTransaction('2')
        self.assertEqual(self.atm.currentAccount.OpeningBalance, 450.90)

        self.atm.login('001')
        mockedInput.side_effect = ['1', '10000']
        self.atm.selectTransaction('2')
        self.assertIsNone(self.atm.currentAccount)

        self.atm.login('001')
        mockedInput.side_effect = ['1', 'h']
        self.atm.selectTransaction('2')
        self.assertIsNone(self.atm.currentAccount)

    def test_updateBalance(self):

        self.atm.currentUser = User('001', 'Alex', 'Bruce', '0404040404')
        self.atm.currentAccount = SavingAccount('001', '123456', 'Saving', 500.50, 1)
        self.atm.updateBalance(50.10)
        self.assertEqual(self.atm.currentAccount.OpeningBalance, 550.6)
        self.atm.updateBalance(-50.20)
        self.assertEqual(self.atm.currentAccount.OpeningBalance, 500.4)

if __name__ == '__main__':
    unittest.main()