import random

import sqlite3

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
    # random.seed()
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
    if summa % 10 == 0:
        luhn = '0'
    else:
        luhn = str(10 - (summa % 10))
    card_number = '400000' + ''.join(card_num) + luhn
    pin_number = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    cur.execute('insert into card(id, number, pin, balance) values (?,?,?,?)', (count, card_number, pin_number, 0))
    cur.execute('select * from card')
    con.commit()
    print(f'''Your card has been created
Your card number:
{card_number}
Your card PIN:
{pin_number}''')


def log_account():
    #card_num = (input('Enter your card number:'))
    card_num = '4000004084321235'
    #card_pin = (input('Enter your PIN:'))
    card_pin = '4532'
    count = 0
    count_m = 0
    for row in cur.execute('select * from card'):
        count += 1
        if row[1] == card_num:
            for row in cur.execute('select * from card where number == ?', (card_num,)):
                if row[2] == card_pin:
                    print('You have successfully logged in!')
                    while True:
                        print('''1. Balance
2. Log out
0. Exit''')
                        #choice = (input())
                        if choice == 1:
                            print('Balance: 0')
                        elif choice == 2:
                            print('You have successfully logged out!')
                            break
                        else:
                            exit()
                else:
                    print('Wrong card number or PIN!')
        else:
            count_m += 1
    if count == count_m:
        print('Wrong card number or PIN!')
    
while True:
    choice = 1
    con = sqlite3.connect('card.s3db')
    cur = con.cursor()
    #cur.execute('drop table card;');
    try:
        cur.execute('create table if not exists card(id INTEGER, number TEXT, pin TEXT, balance INTEGER);')
        con.commit()
        count = 0
    except OperationalError:
        for row in cur.execute('select coalesce(max(id), 0) from card'):
            count = row[0]
    count += 1
    bank_account(choice)
    break


