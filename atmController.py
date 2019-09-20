import os.path
import hashlib

#admin
#eren

# İmzayı değiştirirseniz programdaki kayıtlarıda silmeniz gerekir!!!
programSignature = "7d1c1c8c79b0d0fb619ad978f15f8050695d2a2b2e5611430fde03ca995eaf8b"

def getUsername():
    sys_kullaniciAdi = input(" > Kullanici Adi: ")
    return sys_kullaniciAdi

def getPassword():
    sys_sifre = input(" > Sifre: ")
    return sys_sifre

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

def get_username_from_file(filename):
    usernameTryString = ""
    usernameTryString = usernameTryString + str(read_from_file(filename)[66:130])
    return usernameTryString

def get_password_from_file(filename):
    passwordTryString = ""
    passwordTryString = passwordTryString + str(read_from_file(filename)[132:196])
    return passwordTryString

def get_money_from_file(filename):
    moneyTryString = ""
    moneyTryString = moneyTryString + str(read_from_file(filename)[198:260])
    #print(moneyTryString)
    return moneyTryString

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

# Variable(s)
isLogined = False
isReadedMoney = False
selectedMenuItem = 0
moneyCurrent = 0
paraGonderilebilecekAdamlarinIsimleri = ['YusuFcuk', 'MAli', 'Taloc']

while(True):

    if(check_file_exist('pswd.txt')):

        isFileConfirmed = False

        if(confirm_file_signature("pswd.txt")):
            #print(" > Successfully confirmed file integrity")
            isFileConfirmed = True
        else:
            print(" > Cannot confirm file integrity \n > File erasing...")
            erase_file_details("pswd.txt")
            isFileConfirmed = False

        if not isFileConfirmed:
            print(" > Kullanıcı detayları bulunamadı. \n > Lütfen yeni bir hesap oluşturun.")
            tempUsername, tempPassword = "",""
            tempUsername = getUsername()
            tempPassword = getPassword()
            detailsFile = open("pswd.txt", "a")
            detailsFile.write(programSignature + " \n")
            detailsFile.write(encrypt_string(tempUsername, programSignature) + " \n")
            detailsFile.write(encrypt_string(tempPassword, programSignature) + " \n")
            detailsFile.write("1000") # yeni hesap ise 1000 parayla başlasın
            detailsFile.close()
        else:
            if not isLogined:

                print(" > Lütfen giriş yapınız.")

                tempUsername, tempPassword = "", ""
                tempUsername = getUsername()
                tempPassword = getPassword()

                usernameCorrect = False
                passwordCorrect = False

                if(encrypt_string(tempUsername, programSignature) == get_username_from_file("pswd.txt")):
                    #print("success_username")
                    usernameCorrect = True
                else:
                    #print("not success username")
                    usernameCorrect = False

                if (encrypt_string(tempPassword, programSignature) == get_password_from_file("pswd.txt")):
                    #print("success_password")
                    passwordCorrect = True
                else:
                    #print("not success password")
                    passwordCorrect = False

                if(usernameCorrect):
                    if(passwordCorrect):
                        isLogined = True
                        print("\n > Hoşgeldiniz!\n")
                    else:
                        isLogined = False
                        print(" > Username or password is incorrect.")
                else:
                    isLogined = False
                    print(" > Username or password is incorrect.")

    else:
        print(" > cannot detect file to write")
        erase_file_details("pswd.txt") # yeniden oluşturacaktır

    if(isLogined):
        if not isReadedMoney:
            moneyCurrent = get_money_from_file("pswd.txt")
            #write_money_to_file("pswd.txt", 23525)
            isReadedMoney = True

        if(selectedMenuItem == 0):
            print(" > Bankadaki paranız: "+place_value(int(moneyCurrent))+"TL\n")
            print(" > 1) Para Çekme\n")
            print(" > 2) Para Yatırma\n")
            print(" > 3) Para Gönderme\n")
            tempSelectedItemMenu = input(" > Bir işlem seçiniz (1-3): ")
            if int(tempSelectedItemMenu) < 1:
                print(" > Girdi 1 ile 3 arasında olmalıdır!")
            elif int(tempSelectedItemMenu) > 3:
                print(" > Girdi 1 ile 3 arasında olmalıdır!")
            else:
                selectedMenuItem = int(tempSelectedItemMenu)
        elif(selectedMenuItem == 1):
            print("\n > Bankadaki paranız: "+place_value(int(moneyCurrent))+"TL")
            tempCekilecekMiktar = input("\n > Çekmek istediğiniz miktarı giriniz: ")
            moneyCurrent = int(moneyCurrent) - int(tempCekilecekMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            print("\n > Para çekme işlemi başarılı!\n\n\n")
            selectedMenuItem = 0
        elif(selectedMenuItem == 2):
            print("\n > Bankadaki paranız: " + place_value(int(moneyCurrent)) + "TL")
            tempYatirilacakMiktar = input("\n > Yatırmak istediğiniz miktarı giriniz: ")
            moneyCurrent = int(moneyCurrent) + int(tempYatirilacakMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            print("\n > Para yatırma işlemi başarılı!\n\n\n")
            selectedMenuItem = 0