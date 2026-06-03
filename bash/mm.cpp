/* Assume that a bank that mainitains two kind of accounts for customers
- one is saving
- another currernt

- Saving provide compund intrest and withdarw facilities but no checkbook facility
- the current provide checkbook but no intrest

- current sccount holders should also maintain minimum balance and if balance falls below this level a service charge is imposed

- create a class account that stores customer name , account number and type of account form this derive the classes 
current account and saving account

- include necessary members function in order to achive the foloowing tasks
 1. Accept deposit and update the balance
 2. Display the balance
 3. Compute and deposit intrest 
 4. Permit withdrawl and upadate the balance
 5. check for the minimum balance, impost penality and update the balance

 use memeber funciton to initalize the class members
*/

#include <iostream>
using namespace std;

class Account {
protected:
    string name,acc_no;
    int type;
    float balance;

public:
    Account(string n, int a, string t, float b) {
        name = n;
        acc_no = a;
        type = t;
        balance = b;
    }

    void deposit(float amount) {
        balance += amount;
        cout << "Deposited: " << amount << endl;
    }

    void display() {
        cout << "\nName: " << name << endl;
        cout << "Account No: " << acc_no << endl;
        cout << "Account Type: " << type << endl;
        cout << "Balance: " << balance << endl;
    }
};

class SavingAccount : public Account {
public:
    SavingAccount(string n, int a, float b)
        : Account(n, a, "Saving", b) {}

    void computeInterest(float rate) {
        float interest = balance * rate / 100;
        balance += interest;
        cout << "Interest Added: " << interest << endl;
    }

    void withdraw(float amount) {
        if (balance >= amount) {
            balance -= amount;
            cout << "Withdrawn: " << amount << endl;
        } else {
            cout << "Insufficient Balance!" << endl;
        }
    }
};

class CurrentAccount : public Account {
    float min_balance = 1000;
    float penalty = 100;

public:
    CurrentAccount(string n, int a, float b)
        : Account(n, a, "Current", b) {}

    void withdraw(float amount) {
        if (balance >= amount) {
            balance -= amount;
            cout << "Withdrawn: " << amount << endl;
            checkMinBalance();
        } else {
            cout << "Insufficient Balance!" << endl;
        }
    }

    void checkMinBalance() {
        if (balance < min_balance) {
            cout << "Minimum Balance not maintained!" << endl;
            balance -= penalty;
            cout << "Penalty imposed: " << penalty << endl;
        }
    }
};

int main() {


    SavingAccount s("Medhansh", 101, 5000);
    s.deposit(1000);
    s.computeInterest(5);
    s.withdraw(2000);
    s.display();

    cout << "\n-----------------------------\n";

    CurrentAccount c("Alex", 102, 3000);
    c.deposit(500);
    c.withdraw(2700);
    c.display();

    return 0;
}
