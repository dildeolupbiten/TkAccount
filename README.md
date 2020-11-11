# TkAccount

**TkAccount** is a Python program designed to do some basic accounting operations such as adding categories, products, orders and displaying the orders in a timeline with a cumulative or comparative way.

After downloaded the program, users should see the below files and folders in the main directory of the program.

![img1](https://user-images.githubusercontent.com/29302909/98541507-9aabe380-22a0-11eb-8392-506c713da578.png)

## Availability

Windows, Linux and macOS

## Dependencies

In order to run **TkAccount**, at least [Python](https://www.python.org/)'s 3.6 version must be installed on your computer. Note that in order to use [Python](https://www.python.org/) on the command prompt, [Python](https://www.python.org/) should be added to the PATH. There is no need to install manually the libraries that are used by the program. When the program first runs, the necessary libraries will be downloaded and installed automatically.

## Usage

**1.** Run the program by writing the below to **cmd** for Windows or to **bash** for Unix.

**For Unix**

    python3 run.py

**For Windows**

    python run.py
    
**2.** Short time later a window which is similar to below should be seen.

![img2](https://user-images.githubusercontent.com/29302909/98542012-51a85f00-22a1-11eb-8afc-8eac85d65a30.png)

**3.** As can be seen on the above image, there are 4 menu cascades called **Add**, **View**, **Plot** and **Help**.

**4.** The **Add** menu cascade has 3 menu buttons called **Category**, **Product** and **Order**.

**4.1.** In the first run of the program, users should first add categories for the products they will create later. If users click the **Product** or **Order** menu buttons before creating the categories, the program will show warning messages that remind the users what they should do. If the **Category** menu button is clicked, a window as below should be created.

![img3](https://user-images.githubusercontent.com/29302909/98676558-cf856c80-236c-11eb-8191-3a02e9dee8fb.png)

As can be seen above, there are two buttons at the top of the window. The green colored plus button is for creating category frames. And the red colored minus button is for removing the selected category frame. So if we click the plus button, a frame as below would be created.

![img4](https://user-images.githubusercontent.com/29302909/98676929-54708600-236d-11eb-9da0-69f1ad0da1cf.png)

The category frame itself also contains a plus button. By clicking this plus button we could create sub categories as below:

![img5](https://user-images.githubusercontent.com/29302909/98677291-df518080-236d-11eb-8c51-53e90aa924f7.png)

As you see each sub category itself also contains a plus button. So we could create a lot of categories and the sub categories of them at the same time which will be like a tree branch structure.

Note that all entries that are created must be filled and the neighbour categories shouldn't have the same text, otherwise users should receive warning messages like below.

![img6](https://user-images.githubusercontent.com/29302909/98820771-aaadf980-243f-11eb-9e18-a329cbee7656.png)

![img7](https://user-images.githubusercontent.com/29302909/98821017-05dfec00-2440-11eb-9106-4db7bfd42f31.png)

In order to delete an entire category frame, the checkbutton of the category that is wanted to be deleted should be checked and the minus button at the top is used. This would delete the sub categories of a selected category too. However if a sub category is wanted to be deleted, the minus button of the parent category should be used.

If we fill the category and sub category fields as can be accepted, we could press the green colored tick button which is at the bottom of the window. Below you are seeing an example of a category tree.

![img8](https://user-images.githubusercontent.com/29302909/98679893-b3d09500-2371-11eb-91cc-12cb816c54c8.png)

**4.2.** After created the categories, we are creating products. In order to do that we are clicking the **Product** menu button of **Add** menu cascade. After we click the **Product** button, a window as below should open.

![img9](https://user-images.githubusercontent.com/29302909/98680317-4a9d5180-2372-11eb-8431-c5f3823f48c9.png)

The functions of the buttons which are at the top of the window are same with the functions of the buttons in **Category** window. So, if we click the plus button, a row for a product would be created as below.

![img10](https://user-images.githubusercontent.com/29302909/98682384-eaf47580-2374-11eb-9490-65832c2d1e71.png)

If we want to delete the product frame, we could click the checkbutton of the frame which is at the left then press the minus button.

In the **Product Category** field, we should select the categories we added before. In the **Product Name** field, we should write the name of product. Then we should write the unit price of the product to the **Unit Price** field. And finally we should fill the **Number Of Products** entry. Note that if non-numerical values are added to the **Unit Price** and **Number Of Products** entries, the characters that are written to this entries would be deleted. The **Total Price** value would be calculated automatically when the **Unit Price** and **Number Of Products** entries are filled correctly.

We could add many products by clicking the plus button. If all entries are filled correctly and if we press the **tick** button which is at the bottom of the window, the products would be added to the database. If we forgot to fill an entry of any row, the color of the related entry would colored to red as below.

![img11](https://user-images.githubusercontent.com/29302909/98821250-5c4d2a80-2440-11eb-9cd9-d85ce0587d27.png)

**4.3.** After created the products, we could create orders. In order to do that, we should click the **Orders** menu button of **Add** menu cascade. When we click this button, a window as below should open.

![img12](https://user-images.githubusercontent.com/29302909/98687269-9b18ad00-237a-11eb-9736-5a6ad34b71a0.png)

This window has two parts. One part which is at the top of this window, is for writing the customer information. The other part is for adding products which are ordered by this customer. Customers and their ordered products will be stored in the database. So, if this is the first time we add a customer,we should type the **Name** and the **Email** of the customer by hand. However if there's a customer that is already been in the database, we could type a letter or a word, then we could press to **Enter** key. After that a drop down menu would occur. This drop down menu contains all customers whose name starts with characters we wrote to the **Name** entry and we could select the customer from this list. After we selected the customer, the information of the customer would be inserted to the **Name** and **Email** entries.

![img13](https://user-images.githubusercontent.com/29302909/98688501-f7c89780-237b-11eb-8d13-53f41b2f84fe.png)

In order to add products that are ordered by this customer, we should click the green colored plus button. After that a frame would be created as below.

![img14](https://user-images.githubusercontent.com/29302909/98688794-4b3ae580-237c-11eb-8a76-dfc3ce1d8b26.png)

We could also enlarge the window and/or use scrollbars to see the parts which are unseen of the added product.

![img15](https://user-images.githubusercontent.com/29302909/98689162-b4225d80-237c-11eb-9061-d1c796cd8388.png)

As you see this frame contains a checkbutton which is the left of the frame. We could delete this frame via selecting this frame then pressing the minus button.

First, we should select the **Product Category**. Selecting the **Product Category** will change the values of the **Product Name**. Then, we should select the **Product Name**. After selected the **Product Name**, the **Unit Price** of this product would be inserted to the **Unit Price** entry. And the state of this entry is readonly. Then we should write the **Number Of Products** that the customer is ordered. If the value that is written to this entry is greater than the **Number Of Products** of the stock in the database, we would receive a warning message like below and the entry field would be cleared.

![img16](https://user-images.githubusercontent.com/29302909/98690583-247dae80-237e-11eb-8389-9ef9fd05ad04.png)

According to the image below, the greatest value we could write to the **Number Of Products** entry for this product is **39**. If we type **39** to the **Number Of Products** entry, that would mean, all stock for this products would be sold to this customer. And the stock number would become **0**. And this product would be deleted from our stock database. The database of the program is relational. So the stock numbers of the products would be updated when they are sold.

The entry which comes after **Number Of Products** is for specifying the **Discount** that we want to make. And at the right of the **Discount** entry, we are seeing the **Gain** entry. To this entry, we are writing the value that means how much gain we want to have. After filled these entries, the values of **Total Price** and **Total Gain** would be calculated and be inserted to related entries. Note that we should fill all entries here too. Below you see a correct example of an order.

![img17](https://user-images.githubusercontent.com/29302909/98692361-16309200-2380-11eb-80a3-0d5384054922.png)

Finally, we should click the tick button at the bottom and apply the order.

**5.** When we come to the **View** menu cascade, we would see 3 menu buttons called **Orders**, **Products** and **Purchases**. Each menu button would open records that are stored in the database. We could also change values of selected items.

**5.1.** The **Orders** menu button would open the below window.

![img18](https://user-images.githubusercontent.com/29302909/98699545-5136c380-2388-11eb-97db-e06f3ab98218.png)

In the example above, we are seeing records of a test database.

We could select a row from the treeview and then if we use the right click of the mouse, a right click menu opens that has only one option called **Edit**. The **Edit** option would open a new window as below:

![img19](https://user-images.githubusercontent.com/29302909/98700680-81329680-2389-11eb-9d3f-a382d0d7e4fe.png)

As you see above, the opened window contains values that are stored in the database. If we change values that are written to entries and then press the tick button, the changes will be applied to tables which are relational in the database.

Briefly, if any change is done on order records, this could effect **Product (Stocks)** records also. For example, if we change **Number Of Products** of a product that a customer is bought, **Number Of Products** and **Total Price** of this product would be changed in the **Products (Stocks)** table. Or if we change the **Product Name**, this time, the previous order would be canceled, the **Number Of Products** value of the canceled product would be restored in the **Products (Stocks)** table, the **Total Price** would be re-calculated and finally the **Number of Products** and the **Total Price** of the new product would be changed in the **Products (Stocks)** table.

Changing the **Customer Name**, the **Discount** and the **Gain** values has no effect on the **Products (Stocks)** table but has effect on the **Orders** table.

**5.2.** The **Products** menu button opens the window below.

![img20](https://user-images.githubusercontent.com/29302909/98702935-0c149080-238c-11eb-9352-1ca4e05e454d.png)

As we could change values of records in **Orders** table, we could also change values of records in **Products** table. So, we need to use the right click of the mouse to **Edit** a record. After clicked the **Edit** option, a window as below should open.

![img21](https://user-images.githubusercontent.com/29302909/98703370-7af1e980-238c-11eb-9d92-9baf00a37ce3.png)

Note that the change would only effect the **Products** table.

As mentioned before, **Number Of Products** and the **Total Price** values of the products would change when users create orders. And finally the product which **Number Of Products** become **0** would be deleted from the **Products** table. That means, we ne longer have this product in our stocks.

**5.3** The **Purchases** menu button open the below window.

![img22](https://user-images.githubusercontent.com/29302909/98703980-2ac75700-238d-11eb-9de6-069305df7d96.png)

We could also change values of records in **Purchases** table. However this has no effect upon **Products** and **Orders** tables. In the first time we added products, the **Purchases** and **Products** tables would contain same items. However, when we start adding orders, values of products in the **Products** table would change. So, the **Purchases** table shows products that we purchased in time.

In order to edit a record, we should do same things that are described above.

**6.** The **Plot** menu cascade contains two menu buttons called **Products** and **Customers**. The **Products** menu button is for plotting graphs based on products whereas the **Customers** menu button is for plotting graphs based on customers.

**6.1.** If we click the **Products** menu button, we should see a window like below:

![img23](https://user-images.githubusercontent.com/29302909/98705276-9827b780-238e-11eb-94fe-e86d40fccab8.png)

As can be seen above, the opened window is separated into two frames vertically. The left frame is the frame we make our selections, the right frame is the frame that graphs would be displayed.

We could select one or more than one products from the treeview. Then we should select a checkbutton from the checkbutton groups. 

**Cumulative** and **Comparative** checkbuttons belong to one checkbutton group. Both of them can not be selected at the same time.

**Number Of Products** and **Price** checkbuttons belong to another checkbutton group. Like the other checkbutton group, both of them can not be selected at the same time.

When we click the **Comparative** checkbutton, a new checkbutton group is created as below.

![img24](https://user-images.githubusercontent.com/29302909/98706785-50a22b00-2390-11eb-913b-c212f290ce88.png)

So, **Bar** and **Timeline** checkbuttons are another checkbutton group that will be created if we select **Comparative** checkbutton. If we select **Cumulative** checkbutton, the checkbutton group for **Bar** and **Timeline** would be deleted.

Under the checkbuttons, we see three entry fields. The first entry is related to the time unit that we want to use in the graph. This state of this entry is readonly. And it contains 3 values which are **Day**, **Hour** and **Year**.

If we click **From** and **To** entries, a window like below would open.

![img25](https://user-images.githubusercontent.com/29302909/98707377-079ea680-2391-11eb-8ba0-89046bad4950.png)

Note that, the date value of **From** can not be forward than the date value of **To**. Otherwise we would receive a warning message.

Below you see graphs related to following selections:

![img26](https://user-images.githubusercontent.com/29302909/98708437-32d5c580-2392-11eb-8039-17a27d0c681b.png)

Let's change the **Time Unit** as **Month** and take a look at the graph again for the same product and time range.

![img27](https://user-images.githubusercontent.com/29302909/98709000-d921cb00-2392-11eb-9b17-0cbb67627eef.png)

So the above graph shows how many times a specific product is sold during a timeline. If we select the **Price** checkbutton, this time we will see how much a specific product we earned during a specific time range.

![img28](https://user-images.githubusercontent.com/29302909/98709835-f30fdd80-2393-11eb-9685-a3328c9f008f.png)

If we select more products from the treeview, this time we would see how many times a group of products is sold during a timeline or how much we earned from these products.

We could also use **Comparative** checkbutton to compare the products.

![img29](https://user-images.githubusercontent.com/29302909/98710379-9fea5a80-2394-11eb-8e0b-e439f860a86c.png)

Above we see the monthly number of products sold of two products in a specific time range when we select the **Timeline** checkbutton. Let's check the **Bar** checkbutton and look at the graph again.

![img30](https://user-images.githubusercontent.com/29302909/98710789-2ef77280-2395-11eb-9141-7aab8958597f.png)

This graph shows us the comparison of two products regarding the number of of products sold in a specific time range.

Let's select all products:

![img31](https://user-images.githubusercontent.com/29302909/98711041-8990ce80-2395-11eb-991c-9d5f8f46a332.png)

So, it seems between 01.01.2018 and 10.11.2020, the **Chopard** product is the most sold product. Let's look which product brought the most money during this period.

![img32](https://user-images.githubusercontent.com/29302909/98711768-792d2380-2396-11eb-9f26-fe144d3fedd0.png)

It seems that, **U.S. Polo** and **Mikimoto** products brought the most money during this time period even though **Chopard** is the product that is sold most.

**6.2** If we click the **Customers** menu button, we should see a window like below:

![img33](https://user-images.githubusercontent.com/29302909/98807918-6a914b80-242c-11eb-83f4-a9016b2bfc4b.png)

As we see above, this opened window too is separated into two frames vertically. Like we choose the products with in the previous sections, we can choose the **Customers** from the treeview.

![img34](https://user-images.githubusercontent.com/29302909/98809170-3028ae00-242e-11eb-89e4-c5aa576ab8ec.png)

In the picture above, we see the product distribution that are bought by Suzan Wolf between 01.01.2018 and 11.11.2020. And it seems the product that Suzan Wolf bought most is **Royal**. Let's look at the product Suzan Wolf spends the most on.

![img35](https://user-images.githubusercontent.com/29302909/98809891-5e5abd80-242f-11eb-9782-2001f8cd8991.png)

As can be seen above, the product that Suzan Wolf spends most on is **Royal**.

If we select all customers and take a look at the product distribution, the graph we get should be the graph that we saw in the previous section. In that graph **U.S. Polo** was the product that brought most money and **Chopard** should be the product that was sold most.

![img36](https://user-images.githubusercontent.com/29302909/98810461-58b1a780-2430-11eb-9cdc-df25b94c7932.png)

We could also compare which customer bought how much product or which customer spent more money.

![img37](https://user-images.githubusercontent.com/29302909/98810675-9c0c1600-2430-11eb-81ba-bcff694a958e.png)

So according to the picture above, Christine Smith apparently spent the most money between 01.01.2018 and 11.11.2020.

I think, the things that I should mention the graphs is enough. Nevertheless, if you have any problem, you could open an issue in the GitHub page of the program or you could send a mail to me.

**7.** The **Help** menu cascade contains two menu buttons called **About** and **Check for updates**. The **About** menu button, open a tiny window as below.

![img38](https://user-images.githubusercontent.com/29302909/98811705-518b9900-2432-11eb-938f-2669598a36a2.png)

If any update is released, users could update their program by clicking the **Check for updates** menu button.

## Licenses

**TkAccount** is released under the terms of the **GNU GENERAL PUBLIC LICENSE**. Please refer to the **LICENSE** file.
