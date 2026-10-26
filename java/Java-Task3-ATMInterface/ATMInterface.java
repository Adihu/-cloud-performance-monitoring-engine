import java.util.ArrayList;
import java.util.Scanner;

class BankAccount {
    String userId;
    String userPin;
    double balance;
    ArrayList<String> history;

    public BankAccount(String id, String pin, double initialBalance) {
        userId = id;
        userPin = pin;
        balance = initialBalance;
        history = new ArrayList<>();
        history.add("Account initialized with balance: $" + initialBalance);
    }
}

public class ATMInterface {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // Default test account
        BankAccount account = new BankAccount("admin123", "1234", 1000.0);

        System.out.println("=== WELCOME TO THE ATM ===");
        System.out.print("Enter User ID: ");
        String inputId = scanner.nextLine();
        System.out.print("Enter PIN: ");
        String inputPin = scanner.nextLine();

        if (inputId.equals(account.userId) && inputPin.equals(account.userPin)) {
            System.out.println("\nLogin Successful!\n");
            boolean running = true;

            while (running) {
                System.out.println("--- ATM Menu ---");
                System.out.println("1. Transactions History");
                System.out.println("2. Withdraw");
                System.out.println("3. Deposit");
                System.out.println("4. Transfer");
                System.out.println("5. Quit");
                System.out.print("Choose an option (1-5): ");
                
                int choice = scanner.nextInt();

                switch (choice) {
                    case 1:
                        System.out.println("\n--- Transaction History ---");
                        for (String record : account.history) {
                            System.out.println(record);
                        }
                        System.out.println();
                        break;

                    case 2:
                        System.out.print("Enter amount to withdraw: $");
                        double withdrawAmount = scanner.nextDouble();
                        if (withdrawAmount > account.balance) {
                            System.out.println("Error: Insufficient balance!\n");
                        } else {
                            account.balance -= withdrawAmount;
                            account.history.add("Withdrawn: $" + withdrawAmount);
                            System.out.println("Successfully withdrawn $" + withdrawAmount + "\n");
                        }
                        break;

                    case 3:
                        System.out.print("Enter amount to deposit: $");
                        double depositAmount = scanner.nextDouble();
                        account.balance += depositAmount;
                        account.history.add("Deposited: $" + depositAmount);
                        System.out.println("Successfully deposited $" + depositAmount + "\n");
                        break;

                    case 4:
                        System.out.print("Enter recipient account name: ");
                        scanner.nextLine(); // consume newline
                        String recipient = scanner.nextLine();
                        System.out.print("Enter amount to transfer: $");
                        double transferAmount = scanner.nextDouble();
                        if (transferAmount > account.balance) {
                            System.out.println("Error: Insufficient balance for transfer!\n");
                        } else {
                            account.balance -= transferAmount;
                            account.history.add("Transferred $" + transferAmount + " to " + recipient);
                            System.out.println("Successfully transferred $" + transferAmount + " to " + recipient + "\n");
                        }
                        break;

                    case 5:
                        running = false;
                        System.out.println("Thank you for using the ATM. Goodbye!");
                        break;

                    default:
                        System.out.println("Invalid choice. Please select between 1 and 5.\n");
                }
            }
        } else {
            System.out.println("Authentication Failed! Incorrect User ID or PIN.");
        }
        scanner.close();
    }
}