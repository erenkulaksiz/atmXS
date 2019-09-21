import os.path
import hashlib


programSignature = "7d1c1c8c79b0d0fb619ad978f15f8050695d2a2b2e5611430fde03ca995eaf8b"


def getUsername():
    sys_username = input(" > Username: ")
    return sys_username


def getPassword():
    sys_password = input(" > Password: ")
    return sys_password


def check_file_exist(filename):
    isFileExist = os.path.exists(filename)
    return isFileExist


def erase_file_details(filename):
    fileToErase = open(filename, "w").close()


def read_from_file(filename):
    fileToRead = open(filename, "r")
    return fileToRead.read()


def confirm_file_signature(filename):
    signatureTryString = ""
    signatureTryString = signatureTryString + str(read_from_file(filename)[0:64])
    if (signatureTryString == programSignature):
        return True
    else:
        return False

def get_part_from_file(filename, partmin, partmax):
    thingToGet = ""
    thingToGet = thingToGet + str(read_from_file(filename)[partmin:partmax])
    return thingToGet

# username 66:130
# password 132:196
# money 198:260

def write_money_to_file(filename, value):
    fileToRead = open(filename, "r")
    data = fileToRead.readlines()
    data[3] = str(value)
    fileToWrite = open(filename, "w")
    fileToWrite.writelines(data)


def encrypt_string(hash_string, input_salt):
    hash_string = hash_string + input_salt
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def place_value(number):
    return ("{:,}".format(number))


isLogined = False
isReadedMoney = False
selectedMenuItem = 0
moneyCurrent = 0
peopleList = ['YusuFcuk', 'MAli', 'Taloc', 'gullu']

# This is main loop
while(True):


    if check_file_exist('pswd.txt'):

        isFileConfirmed = False

        if confirm_file_signature("pswd.txt"):
            isFileConfirmed = True
        else:
            print(" > Cannot confirm file integrity \n > File erasing...")
            erase_file_details("pswd.txt")
            isFileConfirmed = False

        if not isFileConfirmed:

            print(" > Cannot found user details. \n > Please create a new account.")
            tempUsername, tempPassword = "", ""
            tempUsername, tempPassword = getUsername(), getPassword()
            detailsFile = open("pswd.txt", "a")
            detailsFile.write(programSignature + " \n")
            detailsFile.write(encrypt_string(tempUsername, programSignature) + " \n")
            detailsFile.write(encrypt_string(tempPassword, programSignature) + " \n")
            detailsFile.write("10000") # This is default starting money.
            detailsFile.close()

        else:

            if not isLogined:

                print(" > Please sign in")

                tempUsername, tempPassword = "", ""
                tempUsername = getUsername()
                tempPassword = getPassword()

                usernameCorrect = False
                passwordCorrect = False

                if encrypt_string(tempUsername, programSignature) == get_part_from_file("pswd.txt", 66, 130):
                    usernameCorrect = True
                else:
                    usernameCorrect = False

                if encrypt_string(tempPassword, programSignature) == get_part_from_file("pswd.txt", 132, 196):
                    passwordCorrect = True
                else:
                    passwordCorrect = False

                if usernameCorrect:
                    if passwordCorrect:
                        isLogined = True
                        print("\n > Welcome!\n")
                    else:
                        isLogined = False
                        print(" > Username or password is incorrect.")
                else:
                    isLogined = False
                    print(" > Username or password is incorrect.")

    else:
        #print(" > Cannot detect a file to write")
        erase_file_details("pswd.txt")

    if isLogined:

        if not isReadedMoney:
            moneyCurrent = get_part_from_file("pswd.txt", 198, 260)
            isReadedMoney = True

        if selectedMenuItem == 0:

            print(" > Money in the bank: "+place_value(int(moneyCurrent))+"$\n")
            print(" > 1) Withdraw money\n")
            print(" > 2) Deposit money\n")
            print(" > 3) Send money\n")
            tempSelectedItemMenu = input(" > Select an option (1-3): ")
            if int(tempSelectedItemMenu) < 1:
                print(" > The entered option must be between 1 and 3!")
            elif int(tempSelectedItemMenu) > 3:
                print(" > The entered option must be between 1 and 3!")
            else:
                selectedMenuItem = int(tempSelectedItemMenu)

        elif selectedMenuItem == 1:

            print("\n > Money in the bank: "+place_value(int(moneyCurrent))+"$")
            tempCekilecekMiktar = input("\n > Enter a value to withdraw: ")
            moneyCurrent = int(moneyCurrent) - int(tempCekilecekMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            print("\n > Withdraw success!\n\n\n")
            selectedMenuItem = 0

        elif selectedMenuItem == 2:

            print("\n > Money in the bank: "+place_value(int(moneyCurrent))+"$")
            tempYatirilacakMiktar = input("\n > Enter a value to deposit: ")
            moneyCurrent = int(moneyCurrent) + int(tempYatirilacakMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            print("\n > Deposit success!\n\n\n")
            selectedMenuItem = 0

        elif selectedMenuItem == 3:

            for x in range(len(peopleList)):
                print(" > "+str(x+1)+") "+str(peopleList[x]))
            tempSelectedSendMoney = input(" > Please select someone to send money (1-"+str(len(peopleList))+"): ")
            tempSendMoneyMiktar = input(" \n >  Enter a value to send money to "+peopleList[int(tempSelectedSendMoney)-1]+":")
            print("\n >  You sent "+str(place_value(int(tempSendMoneyMiktar)))+"$ to "+peopleList[int(tempSelectedSendMoney)-1]+".\n")
            moneyCurrent = int(moneyCurrent) - int(tempSendMoneyMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            selectedMenuItem = 0