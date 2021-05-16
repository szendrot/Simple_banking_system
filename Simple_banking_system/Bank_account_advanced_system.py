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
    cur.execute('insert into card(id, number, pin, balance) values (?,?,?,0)', (count, card_number, pin_number))
    cur.execute('select * from card')
    con.commit()
    print(f'''Your card has been created
Your card number:
{card_number}
Your card PIN:
{pin_number}''')

def log_account():
    #card_num = (input('Enter your card number:'))
    card_num = '4000000876466154'
    #card_pin = (input('Enter your PIN:'))
    card_pin = '0327'
    num1 = 0
    num2 = 0
    for row in cur.execute('select * from card'):
        num1 += 1
        if row[1] == card_num:
            for row in cur.execute('select * from card where number == ?', (card_num,)):
                if row[2] == card_pin:
                    print('You have successfully logged in!')
                    while True:
                        print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
                        #choice = int(input())
                        choice = 3
                        for row in cur.execute('select balance from card where number == ?', (card_num,)):
                                balance = row[0]
                        if choice == 1:
                            print(f'Balance: {balance}')
                            break #it must be deleted
                        elif choice == 2:
                            add_income(card_num, balance)
                            break #it must be deleted
                        elif choice == 3:
                            do_transfer(card_num, card_pin, balance)
                            break #it must be deleted
                        elif choice == 4:
                            print('The account has been closed!')
                            cur.execute('delete from card where number == ?', (card_num,))
                            con.commit()
                            break
                        elif choice == 5:
                            print('You have successfully logged out!')
                            break
                        else:
                            exit()
                else:
                    print('Wrong card number or PIN!')
        else:
            num2 += 1
    if num1 == num2:
        print('Wrong card number or PIN!')

def add_income(card_num, balance):
    for row in cur.execute('select balance from card where number == ?', (card_num,)):
        balance = row[0]
        balance += 15500 #int(input('Enter income'))
        cur.execute('update card set balance = ? where number == ?', (balance, card_num,))
        con.commit()
        print('Income was added!')

def do_transfer(card_num, card_pin, balance):
    print('Transfer')
    #trans_num = input('Enter card number:')
    trans_num = '4000008738420764'
    cur.execute('select * from card where number == ?', (trans_num,))
    data = cur.fetchone()
    card_num_list = []
    card_sum = []
    for i in range(len(trans_num) - 1):
        if i % 2 == 0:
            num2 = 2 * int(list(trans_num)[i])
        else:
            num2 = int(list(trans_num)[i])
        if num2 > 9:
            num2 = num2 - 9
        card_num_list.append(list(trans_num)[i])
        card_sum.append(num2)
    summa = sum(card_sum)
    if summa % 10 == 0:
        luhn = '0'
    else:
        luhn = str(10 - (summa % 10))
    trans_num_m = ''.join(card_num_list) + luhn
    if trans_num == card_num:
        print("You can't transfer money to the same account!")
    elif trans_num != trans_num_m:
        print('Probably you made a mistake in the card number. Please try again!')
    elif data is None:
        print('Such a card does not exist.')
    else:
        #trans_sum = int(input('Enter how much money you want to transfer:'))
        trans_sum = 50
        for row in cur.execute('select balance from card where number == ?', (trans_num,)):
            trans_balance = row[0]
        if balance < trans_sum:
            print('Not enough money!')
        else:
            balance -= trans_sum
            trans_balance += trans_sum
            cur.execute('update card set balance = ? where number == ?', (balance, card_num,))
            cur.execute('update card set balance = ? where number == ?', (trans_balance, trans_num,))
            con.commit()
            print('Success!')
  
while True:
    #choice = int(input())
    choice = 2
    con = sqlite3.connect('card.s3db')
    cur = con.cursor()
    #cur.execute('drop table card;');
    try:
        cur.execute('create table card(id INTEGER, number TEXT, pin TEXT, balance INTEGER);')
        con.commit()
        count = 0
    except sqlite3.OperationalError:
        for row in cur.execute('select coalesce(max(id), 0) from card'):
            count = row[0]
    count += 1
    bank_account(choice)
    break

print('''
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
''')
for row in cur.execute('select * from card'):
    print(row)


