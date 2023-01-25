import pandas as pd

class User:
    def __init__(self, ownerID,firstname,surname,mobile):
        self.ownerID = ownerID
        self.firstname = firstname
        self.surname = surname
        self.mobile = mobile
class ChequeAccount:
    def __init__(self, ownerID,accNum,type,bal,accountDBIndex):
        self.ownerID = ownerID
        self.accNum = accNum
        self.type = type
        self.bal = bal
        self.index = accountDBIndex

class SavingAccount:
    def __init__(self, ownerID,accNum,type,bal,accountDBIndex):
        self.ownerID = ownerID
        self.accNum = accNum
        self.type = type
        self.bal = bal
        self.index = accountDBIndex

#account = ""
#user = ""

def importData():
    importedAccountData = pd.read_csv('data/OpeningAccountsData.txt', skiprows=0, sep='\|\|\|', engine='python')
    importedUserData = pd.read_csv('data/UserInfo.txt')

    return importedAccountData, importedUserData
    #a = data.query("AccountOwnerID == 3")
    #print(data["AccountType"].values)

accountData, userData = importData()

def getUserInformation(userID):
    currentUserData = userData.query("AccountOwnerID == @userID")
    #print(len(currentUserData.index))
    if len(currentUserData.index) == 0:
        return False
    print((currentUserData[["FirstName", "Surname", "Mobile"]].values)[0])
    firstname, surname, mobile = (currentUserData[["FirstName", "Surname", "Mobile"]].values)[0]

    return User(userID,firstname,surname,mobile)

def getAccountInformation(userID):
    currentAccountsData = accountData.query("AccountOwnerID == @userID")
    if len(currentAccountsData.index) == 0:
        return False
    accountOwnerID = currentAccountsData["AccountOwnerID"].values
    accountNumber = currentAccountsData["AccountNumber"].values
    accountType = currentAccountsData["AccountType"].values
    accountOpeningBalance = currentAccountsData["OpeningBalance"].values
    accountIndex = currentAccountsData.index
    accountsList = []
    for index in range(0,len(currentAccountsData.index)):
        if accountType[index] == "Saving":
            savingsAccount = SavingAccount(accountOwnerID[index],accountNumber[index],accountType[index],accountOpeningBalance[index],accountIndex[index])
            accountsList.append(savingsAccount)
        else:
            chequeAccount = SavingAccount(accountOwnerID[index], accountNumber[index], accountType[index], accountOpeningBalance[index],accountIndex[index])
            accountsList.append(chequeAccount)

    return accountsList
def processDepWithd(amount, account):
    account.bal = account.bal + amount
    updateData(account)
def processDeposit(amount,account):
    account.bal = account.bal + amount
    updateData(account)

def processWithdrawal(amount,account):
    account.bal = account.bal - amount
    updateData(account)
def updateData(account):
    updatedData = pd.DataFrame([[account.ownerID,account.accNum,account.type,account.bal]],index=[account.index],columns=accountData.columns)
    accountData.update(updatedData)
    print("Account Summary:\n\tAccount: {} ({})\n\tBalance: {}".format(account.accNum,account.type,account.bal))
def quitSequence(accountData):
    print(accountData)
    # Take accountData and send it to the txt file.



while True:
    userID = input("Enter user ID: ")
    if not userID.isdigit():
        print("Wrong Input\nYou did not enter a valid user ID.")
        continue
    currentUser = getUserInformation(int(userID))
    if type(currentUser) == bool:
        print("Wrong Input\nYou did not enter a valid user ID.")
        continue
    print("Welcome, {} {}.\nPlease select an option:\n\t1 for Deposit\n\t2 for Withdraw\n\t3 for Balance\n\tq to Quit")
    transactionOption = input("Option: ")
    if transactionOption == "q":
        quitSequence(accountData)
        break
    elif transactionOption not in ['1','2','3']:
        print("Wrong Input\nYou must enter an option from the given list.\n")
        continue
    accounts = getAccountInformation(int(userID))
    print("Which account would you like to access?")
    for index in range(0,len(accounts)):
        print("\t{} for {} ({})".format(index+1,accounts[index].accNum,accounts[index].type))
    accountOption = input(": ")
    optionList = list((range(1,len(accounts)+1)))
    optionList = [str(option) for option in optionList]
    print(optionList)
    if accountOption not in optionList:
        print("Wrong Input\nYou must enter an option from the given list.\n")
        continue
    else:
        accountOption = int(accountOption)
    account = accounts[accountOption - 1]
    if transactionOption == '1':
        print("Please enter the amount to be deposited.")
        depositAmount = input(": $")
        if not depositAmount.isdigit():
            print("Wrong Input\nYou must enter dollar and cents. (eg: 415.50)")
            continue
        processDepWithd(int(depositAmount), account)
    elif transactionOption == '2':
        print("Please enter the amount to be withdrawn.")
        withdrawAmount = input(": $")
        if not withdrawAmount.isdigit() or int(withdrawAmount) > account.bal or int(withdrawAmount) <= 0:
            print("Wrong Input\nAmount to withdraw is outside balance range of 0 - {} in your {} account.".format(account.bal,account.type))
            continue
        processDepWithd(-int(withdrawAmount),account)
    elif transactionOption == '3':
        print("Balance for {} account: ${}".format(account.type,account.bal))
    continue




