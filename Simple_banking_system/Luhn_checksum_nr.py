import random
card_dict = {}

print('''1. Create an account
2. Log into account
0. Exit''')

def bank_account(choice):
    if choice == 1:
        create_account()
    elif choice == 2:
        log_account()
    elif choice == 0:
        print('Bye!')
        exit()
    
def create_account():
    #random.seed()
    card_num = []
    card_sum = []
    for i in range(7, 16):
        num1 = random.randint(0, 9)
        if i % 2 == 1:
            num2 = 2 * num1
        else:
            num2 = num1
        if num2 > 9:
            num2 = num2 - 9
        card_num.append(str(num1))
        card_sum.append(num2)
    summa = 8 + sum(card_sum)
    luhn = str(10 - (summa % 10))
    card_number = '400000' + ''.join(card_num) + luhn
    pin_number = ''.join([str(random.randint(0, 9)) for i in range(4)])  
    card_dict[card_number] = pin_number
    print(f'''Your card has been created
Your card number:
{card_number}
Your card PIN:
{pin_number}''')
        
def log_account():
    card_num = (input('Enter your card number:'))
    card_pin = (input('Enter your PIN:'))
    try:
        if card_dict[card_num] == card_pin:
            print('You have successfully logged in!')
            while True:
                print('''1. Balance
2. Log out
0. Exit''')
                if choice == 1:
                    print('Balance: 0')
                elif choice == 2:
                    print('You have successfully logged out!')
                    break
                else:
                    exit()
        else:
            print('Wrong card number or PIN!')
    except KeyError:
        print('Wrong card number or PIN!')

while True:
    choice = 1
    bank_account(choice)
    break

