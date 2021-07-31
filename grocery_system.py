import mysql.connector
from datetime import datetime
mydb=mysql.connector.connect(host="localhost",user="root",password="Rubikscube1!",database="grocery_system")
mycursor=mydb.cursor()
# print(mycursor)
class customerDetails:
    def __init__(self, customerName, password):
        self.customerName = customerName
        self.customerPassword = password

    def isAlreadyExistingUser(self):
        mycursor.execute('select customer_id, customer_name, password from customer_details where customer_name like %s', (self.customerName,))
        details = mycursor.fetchall()
        if details[0][1] == self.customerName and details[0][2] == self.customerPassword:
            return details[0][0]

class groceryItems:

    def listingTheGroceryItems(self):
        category = str(input("enter your category"))
        mycursor.execute('select grocery_id, grocery_name, price, offers from grocery_items where category like %s', (category,))
        items = mycursor.fetchall()
        # showing grocery items to customer for the chosen category
        for row in items:
            print('item name:', row[1], ' ','amount:', row[2], ' ', 'offer:', row[3] )

class addItemsToCart:

    def __init__(self, customer_id):
        self.customer_id = customer_id

    def addingItemsToCart(self):
        #making the customer to add the cart items infinitely untill they give no to stop adding the items in cart
        while True:
            isWhetherToAddAnItem = str(input('Do you want to add an item in your cart? If so, Please enter y -> yes or n -> no'))
            if isWhetherToAddAnItem == 'y':
                item_name = str(input('enter your item name'))
                quantity = int(input('enter your item quantity'))

                # getting cost from database table for the selected item
                mycursor.execute('select grocery_id, price from grocery_items where grocery_name like %s', (item_name,))
                fetchedDetails = mycursor.fetchall()

                # multiplying quantity with cost for the chosen item name
                toMultiplyPriceWithQuantity = fetchedDetails[0][1] * quantity;

                mycursor.execute("insert into cart_details(customer_id,grocery_id,quantity,total_cost) values(%s,%s,%s,%s)",
                                 (self.customer_id, fetchedDetails[0][0], quantity, toMultiplyPriceWithQuantity,))
                mydb.commit()

                print('successfully added to your cart')
            else:
                break

class order:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def orderTheItems(self):
        print('do you want to order the items?')
        isWhetherToOrderTheItems = str(input('y -> yes or n -> no'))
        if isWhetherToOrderTheItems == 'y':
            mycursor.execute(' SELECT cart_details.cart_id, grocery_items.grocery_name, cart_details.quantity, cart_details.total_cost, grocery_items.offers FROM cart_details INNER JOIN grocery_items ON cart_details.grocery_id = grocery_items.grocery_id WHERE customer_id like %s',(self.customer_id,))
            cartItems =mycursor.fetchall()
            for i in range(len(cartItems)):
                rowItems = cartItems[i]
                print('cart item',i+1,'.', 'item_name:', rowItems[1], '  quantity:', rowItems[2], '  total_cost:', rowItems[3], '  offer_applied:', rowItems[2]*rowItems[4])
            #making the customer to choose the options to order infinitely untill they exit
            while True:
                cartItemOption = int(input('Enter the option you like to order or type 0 to exit from order'))
                if cartItemOption != 0:
                    cartId = cartItems[cartItemOption - 1][0]
                    paymentMethod = str(input('What is your payment method, 1. online or 2. cod(cash on delivery)'))
                    now = datetime.now()
                    formattedDate = now.strftime('%Y-%m-%d %H:%M:%S')
                    if paymentMethod == 'online':
                        accountHolderName = str(input('Enter your account holder name'))
                        accountNumber = int(input('Enter your account number'))
                        month = int(input('Enter your account valid month'))
                        year = int(input('Enter your account valid year'))
                        ccv = int(input('Enter your account valid ccv'))
                        address = str(input('Enter your address to deliver the order'))
                        recurring = str(input('want to be a recurring this order? y -> yes or n -> no'))
                        mycursor.execute(
                            "insert into order_details(cart_id,payment_method,account_holder_name,account_no,month,year,ccv,recurring,ordered_time,address) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (cartId, paymentMethod, accountHolderName, accountNumber, month, year, ccv, recurring, formattedDate, address, ))
                        mydb.commit()
                    else:
                        address = str(input('Enter your address to deliver the order'))
                        recurring = str(input('want to be a recurring this order? y -> yes or n -> no'))
                        mycursor.execute(
                            "insert into order_details(cart_id,payment_method,recurring,ordered_time,address) values(%s,%s,%s,%s,%s)",
                            (cartId, paymentMethod, recurring, formattedDate, address, ))
                        mydb.commit()

if __name__ == '__main__':
    customerName = str(input("ENTER YOUR NAME"));
    password = str(input("ENTER YOUR PASSWORD"));
    #calling customerDetails class
    customerValidation = customerDetails('kamali', 'qwerty')
    existingUserId = customerValidation.isAlreadyExistingUser()
    if existingUserId:
        #calling groceryItems class
        listTheGroceryItems = groceryItems()
        listTheGroceryItems.listingTheGroceryItems()

        #calling addItemsToCart class
        cartItems = addItemsToCart(existingUserId)
        cartItems.addingItemsToCart()

        #calling order class
        orderItems = order(existingUserId)
        orderItems.orderTheItems()



    else:
        #sign up process
        phoneNumber = int(input("ENTER YOUR PHONE NUMBER"));
        email = str(input("ENTER YOUR EMAIL"));
        location = str(input("ENTER YOUR LOCATION"));
        mycursor.execute("insert into customer_details(customer_name,phone_number,email,location,password) values(%s,%s,%s,%s,%s)",(customerName,phoneNumber,email,location,password,))
        mydb.commit()

