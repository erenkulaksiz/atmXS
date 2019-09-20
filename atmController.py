import os.path
import hashlib


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

            print(" > Kullanıcı detayları bulunamadı. \n > Lütfen yeni bir hesap oluşturun.")
            tempUsername, tempPassword = "", ""
            tempUsername, tempPassword = getUsername(), getPassword()
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

    if isLogined:

        if not isReadedMoney:
            moneyCurrent = get_part_from_file("pswd.txt", 198, 260)
            #write_money_to_file("pswd.txt", 23525)
            isReadedMoney = True

        if selectedMenuItem == 0:

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

        elif selectedMenuItem == 1:

            print("\n > Bankadaki paranız: "+place_value(int(moneyCurrent))+"TL")
            tempCekilecekMiktar = input("\n > Çekmek istediğiniz miktarı giriniz: ")
            moneyCurrent = int(moneyCurrent) - int(tempCekilecekMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            print("\n > Para çekme işlemi başarılı!\n\n\n")
            selectedMenuItem = 0

        elif selectedMenuItem == 2:

            print("\n > Bankadaki paranız: " + place_value(int(moneyCurrent)) + "TL")
            tempYatirilacakMiktar = input("\n > Yatırmak istediğiniz miktarı giriniz: ")
            moneyCurrent = int(moneyCurrent) + int(tempYatirilacakMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            print("\n > Para yatırma işlemi başarılı!\n\n\n")
            selectedMenuItem = 0

        elif selectedMenuItem == 3:

            for x in range(len(peopleList)):
                print(" > "+str(x+1)+") "+str(peopleList[x]))
            tempSelectedSendMoney = input(" > Lütfen para göndermek istediğiniz kişiyi seçiniz (1-"+str(len(peopleList))+"): ")
            tempSendMoneyMiktar = input(" \n > "+peopleList[int(tempSelectedSendMoney)-1]+" kişisine göndermek istediğiniz miktarı girin: ")
            print("\n > "+peopleList[int(tempSelectedSendMoney)-1]+" kişisine "+str(place_value(int(tempSendMoneyMiktar)))+"TL gönderdiniz.\n")
            moneyCurrent = int(moneyCurrent) - int(tempSendMoneyMiktar)
            write_money_to_file("pswd.txt", int(moneyCurrent))
            selectedMenuItem = 0