import numpy as np

class User:
    def __init__(self, AccountOwnerID,firstname,surname,mobile):
        self.AccountOwnerID = AccountOwnerID
        self.firstname = firstname
        self.surname = surname
        self.mobile = mobile

class SavingAccount:
    def __init__(self, AccountOwnerID,AccountNumber,AccountType,OpeningBalance,accountDBIndex):
        self.AccountOwnerID = AccountOwnerID
        self.AccountNumber = AccountNumber
        self.AccountType = AccountType
        self.OpeningBalance = OpeningBalance
        self.accountDBIndex = accountDBIndex

class ChequeAccount:
    def __init__(self, AccountOwnerID,AccountNumber,AccountType,OpeningBalance,accountDBIndex):
        self.AccountOwnerID = AccountOwnerID
        self.AccountNumber = AccountNumber
        self.AccountType = AccountType
        self.OpeningBalance = OpeningBalance
        self.accountDBIndex = accountDBIndex

class ATM:
    def __init__(self, users=[], accounts=[], currentUser=None, currentAccount=None, error=False, exitProgram=False):
        self.users = users
        self.accounts = accounts
        self.currentUser = currentUser
        self.currentAccount = currentAccount
        self.error = error
        self.exitProgram = exitProgram
        print("Nothing")

    def beginTransaction(self):
        self.currentUser = None
        self.currentAccount = None
        self.error = False

    def login(self, userID):
        if not userID.isdigit():
            self.handleError("Hint: Your user ID is a number")
        else:
            for user in self.users:
                print(user.AccountOwnerID)
                if user.AccountOwnerID == userID:
                    print("Welcome, {} {}.\nPlease select an option:\n\t1 for Deposit\n\t2 for Withdraw\n\t3 for Balance\n\tq to Quit".format(user.firstname,user.surname))
                    self.currentUser = user
                    break
            else:
                self.handleError("You did not enter a valid user ID")

    def selectAccount(self, transactionOption):
        if transactionOption == "q":
            self.quitSequence()
        elif transactionOption not in ['1', '2', '3']:
            self.handleError("You must enter an option from the given list.")
        else:
            print("Which account would you like to access.")
            transactionOption = int(transactionOption)
            index = 0
            optionList = []
            listedAccounts = []
            for account in self.accounts:
                print(account.AccountOwnerID)
                if account.AccountOwnerID == self.currentUser.AccountOwnerID:
                    index += 1
                    print("\t{} for {} ({})".format(index, account.AccountNumber, account.AccountType))
                    optionList.append(index)
                    listedAccounts.append(account)
            else:
                accountOption = input(": ")
                if not accountOption.isdigit():
                    self.handleError("You must choose an option from the given list.")
                elif int(accountOption) not in optionList:
                    self.handleError("You must choose an option from the given list.")
                else:
                    self.currentAccount = listedAccounts[int(accountOption)-1]
                    self.handleTransaction(transactionOption)

    def handleTransaction(self,transactionOption):
        if transactionOption == 1:
            self.handleDeposit()
        elif transactionOption == 2:
            self.handleWithdrawal()
        elif transactionOption == 3:
            self.displayBalance()

    def handleDeposit(self):
        print("Please enter the amount to be deposited.")
        depositAmount = input(": $")
        if not depositAmount.isdigit():
            self.handleError("You must enter dollar and cents. (eg: 415.50)")
        else:
            self.updateBalance(int(depositAmount))

    def handleWithdrawal(self):
        print("Please enter the amount to be withdrawn. (Balance = ${})".format(self.currentAccount.OpeningBalance))
        withdrawAmount = input(": $")
        if not withdrawAmount.isdigit() or int(withdrawAmount) > self.currentAccount.OpeningBalance or int(withdrawAmount) <= 0:
            self.handleError("Amount to withdraw is outside balance range of $0 - ${} in your {} account.".format(
                self.currentAccount.OpeningBalance, self.currentAccount.AccountType))
        else:
            self.updateBalance(-int(withdrawAmount))

    def displayBalance(self):
        print("Account Summary:\n\tAccount: {} ({})\n\tBalance: {}\n".format(self.currentAccount.AccountNumber, self.currentAccount.AccountType, self.currentAccount.OpeningBalance))

    def updateBalance(self,amount):
        self.currentAccount.OpeningBalance = self.currentAccount.OpeningBalance + amount
        self.accounts[self.currentAccount.accountDBIndex].OpeningBalance = self.currentAccount.OpeningBalance
        self.displayBalance()

    def handleError(self, message):
        self.error = True
        print("Wrong Input\n{}".format(message))

    def quitSequence(self):
        accountsDataToExport = np.empty([len(self.accounts), 4], dtype=object)

        for row in range(0, len(self.accounts)):
            accountsDataToExport[row][0] = self.accounts[row].AccountOwnerID
            accountsDataToExport[row][1] = self.accounts[row].AccountNumber
            accountsDataToExport[row][2] = self.accounts[row].AccountType
            accountsDataToExport[row][3] = self.accounts[row].OpeningBalance
        print(accountsDataToExport)

        np.savetxt('data/OpeningAccountsData.txt', accountsDataToExport, delimiter="|||", fmt = "%s")
        self.exitProgram = True

    def importData(self):
        importedAccountData = np.genfromtxt('../../data/OpeningAccountsData.txt', delimiter='|||', skip_header=1, dtype="str")
        importedUserData = np.genfromtxt('../../data/UserInfo.txt', delimiter=',', skip_header=1, dtype="str")
        print(importedUserData)
        accountsList = []
        usersList = []
        for index in range(0,len(importedAccountData)):
            if importedAccountData[index][2] == "Saving":
                savingsAccount = SavingAccount(importedAccountData[index][0], importedAccountData[index][1], importedAccountData[index][2], float(importedAccountData[index][3]), int(index))
                accountsList.append(savingsAccount)

            else:
                chequeAccount = ChequeAccount(importedAccountData[index][0], importedAccountData[index][1], importedAccountData[index][2], float(importedAccountData[index][3]), int(index))
                accountsList.append(chequeAccount)
        for index in range(0,len(importedUserData)):
            user = User(importedUserData[index][3], importedUserData[index][0], importedUserData[index][1], importedUserData[index][2])
            usersList.append(user)

        self.accounts = accountsList
        self.users = usersList
        print(len(self.accounts))

    def startAtm(self):
        while True:
            self.beginTransaction()
            userID = input("Enter user ID: ")
            self.login(userID)
            if self.error == True:
                continue
            transactionOption = input(": ")
            listedAccounts = self.selectAccount(transactionOption)
            if self.exitProgram:
                break

        #importedAccountData = pd.read_csv('data/OpeningAccountsData.txt', skiprows=0, sep='\|\|\|', engine='python', dtype={"AccountOwnerID":"str"})
        #importedUserData = pd.read_csv('data/UserInfo.txt',dtype="str")
        #accountOwnerID = importedAccountData["AccountOwnerID"].values
        #accountNumber = importedAccountData["AccountNumber"].values
        #accountType = importedAccountData["AccountType"].values
        #accountOpeningBalance = importedAccountData["OpeningBalance"].values

        #userOwnerID = importedUserData["AccountOwnerID"].values
        #userFirstName = importedUserData["FirstName"].values
        #userSurname = importedUserData["Surname"].values
        #userMobile = importedUserData["Mobile"].values

        #accountIndex = importedAccountData.index
        #userIndex = importedUserData.index
        #accountsList = []
        #usersList = []
        #for index in range(0, len(importedAccountData.index)):
        ###    if accountType[index] == "Saving":
        #        savingsAccount = SavingAccount(accountOwnerID[index], accountNumber[index], accountType[index], accountOpeningBalance[index], accountIndex[index])
        #        accountsList.append(savingsAccount)
        #    else:
        #        chequeAccount = SavingAccount(accountOwnerID[index], accountNumber[index], accountType[index], accountOpeningBalance[index], accountIndex[index])
        #        accountsList.append(chequeAccount)
        #for index in range(0, len(importedUserData.index)):

         #   user = User(userOwnerID[index], userFirstName[index], userSurname[index], userMobile[index])
         #   usersList.append(user)

        #self.accounts = accountsList
        #print(self.accounts[1].AccountType)
        #self.users = usersList
    # a = data.query("AccountOwnerID == 3")
    # print(data["AccountType"].values)

atm = ATM()
atm.importData()

atm.startAtm()
