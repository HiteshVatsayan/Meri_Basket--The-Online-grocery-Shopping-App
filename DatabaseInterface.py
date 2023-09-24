import mysql.connector
import time
from getpass import getpass

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sigma@1.", 
  database="schema1",
  autocommit=True
)


print("DATABASE INTERFACE",end='\n\n')

print("Enter as:\n1.Customer   2.Admin   3.Retail Outlet   4.Delivery Agent   5.Exit\n")
t=int(input())
while t!=5:
    cur=db.cursor()
    if t==1:
        print("CUSTOMER LOGIN")
        email=str(input("enter email ID: "))
        #password=str(input("enter password: "))
        password=getpass("Enter password")
  
        # email="kheims1@apple.com"
        # password="RDyhEn1kL"
        query="select * from customer join cart  on customer_id=cart_cust_id join membership on customer_id=mem_cust_id join schema1.order on customer_id=order_cust_id join items on order_id=item_order_id where email_ID=\'"+email+"\' and account_password=\'"+password+"\'"

        cur.execute(query)
        custdata=cur.fetchall()
        if len(custdata)!=0:
        
            opt2=int(input("1.Manage Profile   2.View Product   3.Exit\n"))
            ordersetFlag=0
            while opt2!=3:
                
                if opt2==1:
                    print("select an option:\n1.View profile details   2.View recent orders   3.View membership status   4.View Cart   5.Exit")
                    i=int(input())
                    while i!=5:
                        if i==1:
                            print("Name: "+custdata[0][1]+" "+custdata[0][2]+" "+custdata[0][3])
                            print("Address: "+custdata[0][5]+", "+custdata[0][6]+", "+custdata[0][7]+", pincode: "+str(custdata[0][8]))
                            print("Phone nos.: "+str(custdata[0][9])+", "+str(custdata[0][10])+", "+str(custdata[0][11]))
                            print("Email ID: "+custdata[0][12])
                        if i==2:
                            cur.execute("select order_id,order_status from schema1.order where order_cust_id="+str(custdata[0][0]))
                            #cur.execute("select * from product join item_ord on product_id=item_ord.itemID")
                            ordersD=cur.fetchall()
                            counter=0
                            for i in ordersD:
                                oid=int(i[0])
                                #cur.execute("select * from item_ord where orderID="+str(oid))
                                cur.execute("select * from schema1.item_ord  where orderID="+str(oid))
                                itemD=cur.fetchall()
                                if len(itemD)!=0:
                                    k=0
                                    for j in itemD:
                                        itD=list(j)
                                        if k!=j[4]:
                                            counter+=1
                                            print("----Order "+str(counter)+"----")
                                        k=j[4]
                                        print("\nItem name: "+itD[1]+"\nQTY: "+str(itD[2])+"\nEffective Price: "+str(itD[3]))
                                        print("Order status: "+str(i[1]))

                           
                        if i==3:
                            if custdata[0][18]==1:
                                print("Membership type:\nStandard")
                            if custdata[0][18]==2:
                                print("Membership type:\nPremium")
                        if i==4:
                            cur.execute("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
                            cartQ="select item_name,effective_price,item_quantity,item_id,item_order_id,item_prod_id from items where item_cart_id="+str(custdata[0][13])+" group by item_name;"
                            cur.execute(cartQ)
                            CartData=cur.fetchall()
                            cartSum=0
                            sno=0
                            for i in CartData:
                                print("----------")
                                sno+=1
                                print("Item id "+str(i[3]))
                                cartSum+=i[1]
                                print("Item Name: ",end="")
                                print(i[0])
                                print("QTY: "+str(i[2]))
                                print("Effective Price: "+str(i[1]))
                            print("Current cart value: ")
                            print(cartSum)
                            if len(CartData)!=0:
                                print("Do you want\n1.Update Item qty\t2.skip")
                                cartopt=int(input())
                                while(cartopt!=2):
                                    if(cartopt==1):
                                        updQ=""
                                        itemid=int(input("Enter Item no. to update: "))
                                        newQ=int(input("Add new quantity: "))
                                        if newQ>3:
                                            print("Can't add more than 3")
                                        elif newQ<0:
                                            print("Invalid")
                                        elif newQ==0:
                                            updQ="delete from items where item_id="+str(itemid)
                                            cur.execute(updQ)
                                            print("Item updated")
                                        else:
                                            updQ="update items set item_quantity="+str(newQ)+" where item_id="+str(itemid)
                                            cur.execute(updQ)
                                            print("Item updated")
                                    print("Do you want\n1.Update Item qty\t2.skip")
                                    cartopt=int(input())
                                
                                checkout=int(input("Do you want to checkout?(1/0) "))
                                if checkout==1:
                                    cur.execute("select * from retailstore where store_address_city=\'"+str(custdata[0][6])+"\'")
                                    retailNear=cur.fetchall()
                                    retailNearIDLi=[]
                                    if len(retailNear)!=0:
                                        for i in retailNear:
                                            retailNearIDLi.append(i[0])
                                        retailNearID=retailNearIDLi[0]
                                        checkOpt=int(input("Select a payment method\n1.Cash on Delivery\t2.Card"))
                                        if checkOpt==2:
                                            cur.execute("Select * from cards where cards.id="+str(custdata[0][0]))
                                            carddata=cur.fetchall()
                                            print("Card details")
                                            print("Card  name: "+str(carddata[0][1]))
                                            print("Card number: "+str(carddata[0][2]))
                                            print("CVV: "+str(carddata[0][3]))
                                            usecase=int(input("1.Use existing card\t2.Add new card"))
                                            if usecase==2:
                                                detail1=str(input("Enter name on card: "))
                                                detail2=int(input("Enter card number"))
                                                detail3=int(input("Enter CVV"))
                                                cur.execute("delete from cards where cards.id="+str(custdata[0][0]))
                                                cur.execute("insert into cards values("+str(custdata[0][0])+", \'"+str(detail1)+"\', \'"+str(detail2)+"\', "+str(detail3)+")")
                                                print("Card updated!")
                                            if usecase==1:
                                                print("Existing card used for payment")
                                            #print("...Payment Initiated!")

                                        cur.execute("select * from payment")
                                        paymentD=cur.fetchall()
                                        newid=len(paymentD)+1
                                        cur.execute("select * from schema1.order")
                                        orderidnew=cur.fetchall()
                                        currenttime=str(time.time())
                                        cur.execute("insert into schema1.order values("+str(len(orderidnew)+1)+",\'"+str(currenttime)+"\',"+str(custdata[0][0])+","+str(retailNearID)+","+str(0)+")")
                                        for i in CartData:
                                            cur.execute("insert into schema1.item_ord values("+str(i[5])+", \'"+str(i[0])+"\', "+str(i[2])+", "+str(i[1])+", "+str(len(orderidnew)+1)+")")
                                        print("Waiting for verification from the outlet...")
                                        print("Proceed to \'Orders\' to view its status")
                                        
                                        # cur.execute("update schema1.order set order_date=\'"+str("2022-04-27 00:38:54")+"\', order_retail_id="+str(retailNearID)+" where order_id="+str(CartData[0][4]))
                                        # cur.execute("insert into schema1.order values( "+str(CartData[0][4]+1)+",\'"+str("2022-04-27 00:38:54")+"\',"+str(custdata[0][0])+", "+str(retailNearID)+")")
                                        
                                        cur.execute("insert into payment values( "+str(newid)+","+str(checkOpt)+","+str(cartSum)+","+str(custdata[0][0])+","+str(len(orderidnew)+1)+" )")
                                        cur.execute("delete from items where item_cart_id="+str(custdata[0][0]))
                                        ordersetFlag=0
                                        
                                    else:
                                        print("No retail outlet found nearby. Please try again later")

                        print("select an option:\n1.View profile details   2.View recent orders   3.View membership status   4.View Cart   5.Exit")
                        i=int(input())

                
                if opt2==2:
                    a=str(input("Search a product: "))
                    print("Choose a filter:\n1.Price   2.Rating   3.no filter")
                    filter=int(input())
                    priceH=10000
                    priceL=0
                    rating=0
                    if filter==1:
                        priceL=str(input("Enter lower price limit:"))
                        priceH=str(input("Enter higher price limit:"))
                    if filter==2:
                        rating=str(input("Enter minimum rating: "))

                    query="select * from product join items on item_prod_id=product_id where product_name LIKE\'%"+str(a)+"%\' and price>="+str(priceL)+" and price<="+str(priceH)+" and rating>="+str(rating)
                    
                    cur.execute(query)
                    proddata=cur.fetchall()
                    count=0
                    if len(proddata)!=0:
                        for i in proddata:
                            count+=1
                            print("\n"+str(count))
                            print("Product ID: "+str(i[0]))
                            print("Product name: "+str(i[1]))
                            print("Product Stock: "+str(i[2]))
                            print("Product price: "+str(i[3]))
                            print("Product rating: "+str(i[4]))
                        prodinp=int(input("Select a product to put in cart (Enter product ID/0 for skipping): "))
                        print("Discounts available:")
                        cur.execute("select * from discount where disc_prod_id="+str(prodinp))
                        discountsD=cur.fetchall()
                        for j in range(len(proddata)):
                                if proddata[j][0]==prodinp:
                                    ind=j
                                    break
                        discID=0
                        if len(discountsD)!=0:
                            for i in discountsD:
                                if i[2]<=custdata[0][18]:
                                    print("discount ID: "+str(i[0])+", discount value: "+str(i[1]))
                            discID=int(input("select a discount (0 for none): "))
                        discVal=0
                        for i in discountsD:
                            if i[0]==discID:
                                discVal=i[1]
                        if discID!=0:
                            effPrice=proddata[ind][3]-discVal
                        else:
                            effPrice=proddata[ind][3]
                        if prodinp!=0:
                            cur.execute("show triggers")
                            triggerD=cur.fetchall()
                            #cur.execute("drop trigger item_qty_check")
                            tflag1=0
                            for i in triggerD:
                                if str(i[0])=="item_qty_check":
                                    tflag1=1
                                    break
                            if tflag1==0:
                                trigquery="create trigger item_qty_check before insert on items for each row begin if new.item_quantity>3 then set new.item_quantity=3; end if; end"
                                cur.execute(trigquery)
                            itemqty=int(input("Enter qty for item: "))
                            if itemqty>3:
                                itemqty=3
                            effPrice*=itemqty
                            print("Effective price is now: "+str(effPrice))
                            cur.execute("select * from items")
                            itemidnew=(cur.fetchall())
                            print(len(itemidnew))
                            if ordersetFlag==0:
                                cur.execute("select count(*) from schema1.order")
                                orderid=cur.fetchall()
                                orderid=str(orderid)
                                orderid=int(orderid[2:5])
                                ordersetFlag=1
                                #cur.execute("insert into schema1.order values("+str(orderid+1)+",0,"+str(custdata[0][0])+",1)")
                            query1="insert into items values("+str(len(itemidnew) +1)+",\'"+str(proddata[ind][1])+"\',"+str(itemqty)+","+str(effPrice)+","+str(custdata[0][13])+","+str(proddata[ind][0])+","+str(orderid)+")"
                            cur.execute(query1)
                            tempquery="select * from items where item_id="+str(len(itemidnew) +1)
                            cur.execute(tempquery)
                            data=cur.fetchall()
                            print("You added the following item in your cart: ")
                            print("item name: "+str(proddata[ind][1])+" Quantity: "+str(data[0][2]))
                            cur.execute("update cart set current_amount=current_amount+"+str(data[0][2])+"*"+str(effPrice))
                    else:
                        print("No products found")
                opt2=int(input("1.Manage Profile   2.View Product   3.Exit\n"))
        else:
            print("Invalid credentials")
    if t==2:
        adminopt=0
        while adminopt!=3:
            adminopt=int(input("Select an option:\n1.Update Product Stock   2.View Business Analytics   3.Exit\n"))
            if adminopt==1:
                cur.execute("show triggers")
                triggerD=cur.fetchall()
                tflag2=0
                for i in triggerD:
                    if str(i[0])=="reduce_price":
                        tflag2=1
                        break
                if tflag2==0:
                    cur.execute("create trigger reduce_price before update on product for each row begin if new.stock<5 then set new.price=old.price*1.1; elseif new.stock>=5 then set new.price=old.price*0.80; end if; end")
                prodid=int(input("Enter product id: "))
                newstock=int(input("Enter new stock: "))
                
                cur.execute("UPDATE product set stock="+str(newstock)+" WHERE product_id="+str(prodid))
                cur.execute("select * from product where product_id="+str(prodid))
                data=cur.fetchall()
                data=data[0]
                print("\n---Record is updated as follows---\n")
                print("Product ID: "+str(data[0]))
                print("Product name: "+data[1])
                print("Product Stock: "+str(data[2]))
                print("Product price: "+str(data[3]))
                print("Product rating: "+str(data[4]))
            if adminopt==2:
                adminopt2=int(input("Select an option to proceed:\n1.Customer geographical density   2.Memberships   3.Delivery agents density   4.Sales by Region\n"))
                if adminopt2==1:
                    olapQ="select customer.address_city,customer.address_state, count(customer.customer_id) from customer group by customer.address_city,customer.address_state with rollup;"
                    a="City"
                    b="State"
                    c="Number of Customers"
                if adminopt2==2:
                    olapQ="select membership_validity,membership_type, count(mem_cust_id) from membership group by membership_validity, membership_type with rollup;"
                    a="Validity"
                    b="Type"
                    c="Number of Customers"
                if adminopt2==3:
                    olapQ="select deliveryagent.location_city as 'Location City',deliveryagent.location_state as 'Location State' , count(deliveryagent.agent_id) as 'Number of Agents' from deliveryagent group by deliveryagent.location_city,deliveryagent.location_state with rollup;"
                    a="City"
                    b="State"
                    c="Number of delivery agents"
                if adminopt2==4:
                    olapQ="select retailstore.store_address_city as 'City',retailstore.store_address_state as 'State',sum(effective_price) from retailstore join schema1.order on order_retail_id=retail_id join items on item_order_id=order_id group by retailstore.store_address_city,retailstore.store_address_state with rollup;"
                    a="City"
                    b="State"
                    c="Number of stores"
                cur.execute(olapQ)
                badata=cur.fetchall()
                count=0
                maxn=0
                minn=2000
                for i in badata:
                    if str(i[1])!='None' and str(i[0])!='None':
                        count+=1
                        print("Sno.: "+str(count))
                        print(a+": "+str(i[0]))
                        print(b+": "+str(i[1]))
                        print(c+": "+str(i[2]))
                        if maxn<i[2]:
                            maxn=i[2]
                            city=i[0]
                            state=i[1]
                        if minn>i[2]:
                            minn=i[2]
                            mincity=i[0]
                            minstate=i[1]
                print("---Maximum in---")
                print(str(city)+" "+" "+str(state)+" : "+str(maxn))
                print("---Minimum in---")
                print(str(mincity)+" "+" "+str(minstate)+" : "+str(minn))
    if t==3:
        retId=str(input("Enter UserID: "))
        #retPass=str(input("Enter password: "))
        retPass=getpass("Enter password")
        # retId="rpandyagn@dmoz.org"
        # retPass="MXlg05ak"
        cur.execute("select * from retailstore where email_ID=\'"+str(retId)+"\' and account_password=\'"+str(retPass)+"\'")
        retData=cur.fetchall()
        retopt=int(input("Select an option\n1.Manage Orders\t2.Set deals/discounts\t3.Exit"))
        while retopt!=3:
            if retopt==1:
                ordopt=1
                while(ordopt!=3):
                    ordopt=int(input("1.Order History\t2.Order Requests"))
                    if ordopt==1:    
                        cur.execute("select * from schema1.order join item_ord on item_ord.orderID=schema1.order.order_id where order_retail_id="+str(retData[0][0])+" and order_status="+str(1))
                        retOrd=cur.fetchall()
                        sorted(retOrd,key=lambda s:int(s[0]))
                        temp=0
                        for ele in retOrd:
                            if temp!=ele[0]:
                                print("Order ID: "+str(ele[0]))
                            temp=ele[0]
                            print("Item name: "+str(ele[6]))
                            print("Item quantity: "+str(ele[7]))
                            print("Effective price for Item: "+str(ele[8]))
                    if ordopt==2:    
                        cur.execute("select * from schema1.order join item_ord on item_ord.orderID=schema1.order.order_id where order_retail_id="+str(retData[0][0])+" and order_status="+str(0))
                        retOrd=cur.fetchall()
                        temp=0
                        for ele in retOrd:
                            if temp!=ele[0]:
                                print("Order ID: "+str(ele[0]))
                            temp=ele[0]
                            print("Item name: "+str(ele[6]))
                            print("Item quantity: "+str(ele[7]))
                            print("Effective price for Item: "+str(ele[8]))

                        if len(retOrd)==0:
                            print("No requests")
                        if len(retOrd)!=0:
                            action=int(input("Select an orderID to perform action (0 for skipping): "))
                            if action:
                                orderact=int(input("Accept-1 or Reject-0" ))
                                if orderact==1:
                                    cur.execute("update schema1.order set order_status="+str(1)+" where order_id="+str(action))
                                    
                                    print("Order Accepted")

                                    cur.execute("Select * from deliveryagent where location_city=\'"+str(retData[0][3])+"\'")
                                    agentNear=cur.fetchall()
                                    cur.execute("select * from delivery_req")
                                    delnewid=cur.fetchall()
                                    for i in agentNear:
                                        cur.execute("insert into delivery_req values("+str(len(delnewid)+1)+","+str(i[0])+",0,"+str(action)+")")

                                else:
                                    cur.execute("update schema1.order set order_status="+str(0)+" where order_id="+str(action))
                                    cur.execute("insert into ret_ord_rej values("+str(retData[0][0])+","+str(action)+")")
                                    print("Order Rejected")
                                    cur.execute("select * from retailstore where store_address_city=\'"+str(retData[0][3])+"\'")
                                    newretids=cur.fetchall()
                                    for retids in newretids:
                                        cur.execute("select * from ret_ord_rej where ID_retail="+str(retids[0])+" and ID_order="+str(action))
                                        ordverify=cur.fetchall()
                                        if len(ordverify)==0:
                                            cur.execute("select * from schema1.order where order_id="+str(action))
                                            newretOrdD=cur.fetchall()
                                            cur.execute("update schema1.order set order_retail_id="+str(retids[0])+" where order_id="+str(action))

            if retopt==2:
                disc1=float(input("Enter discount value: "))
                disc2=int(input("Enter discount type: "))
                disc3=int(input("Enter product ID: "))
                cur.execute("select * from discount")
                discIDnew=cur.fetchall()
                cur.execute("insert into discount values("+str(len(discIDnew)+1)+","+str(disc1)+","+str(disc2)+","+str(retData[0][0])+","+str(disc3)+")")
                print("Discount added")
            retopt=int(input("Select an option\n1.Orders Received\t2.Set deals/discounts   3.Exit"))
    if t==4:
        # agentId="24"
        # agentPass="wJ7k88qJd"
        agentId=str(input("Enter ID: "))
        #agentPass=str(input("Enter password: "))
        agentPass=getpass("Enter password")
        cur.execute("select * from deliveryagent where agent_id="+str(agentId)+" and account_password=\'"+str(agentPass)+"\'")
        agentD=cur.fetchall()
        if len(agentD)!=0:
            delopt=int(input("1.Delivery Requests   2.Delivery History   3.Mark an ongoing delivery as done"))
            if delopt==1:
                cur.execute("select * from delivery_req where deli_agent_id="+str(agentId)+" and deli_req=0")
                delreq=cur.fetchall()
                if len(delreq)!=0:
                    for reqs in delreq:
                        print("delivery ID: "+str(reqs[0]))
                        print("Order ID to be delivered: "+str(reqs[3]))
                        
                    reqid=int(input("Enter a delivery request ID to perform action (0 for skipping): "))
                else:
                    reqid=0
                    print("No requests")
                if reqid!=0:
                    reqdel=int(input("1.Accept   2.Reject"))
                    if reqdel==1:
                        cur.execute("update delivery_req set deli_req=1 where deli_agent_id="+str(agentId)+" and deli_id="+str(reqid))
                        cur.execute("delete from delivery_req where deli_id="+str(reqid)+" and deli_req=0")

                        cur.execute("select * from delivery_req where deli_agent_id="+str(agentId)+" and deli_id="+str(reqid))
                        delidata=cur.fetchall()
                        delidata=list(delidata[0])

                        cur.execute("select * from delivery")
                        deliveryid=cur.fetchall()
                        currenttimedel=str(time.time())
                        cur.execute("insert into delivery values("+str(len(deliveryid)+1)+",\'"+str(currenttimedel)+"\',"+str(0)+","+str(agentId)+","+str(delidata[3])+")")
                        print("Delivery accepted!")
                    if reqdel==2:
                        cur.execute("delete from delivery_req where deli_id="+str(reqid)+" and deli_agent_id="+str(agentId))
                        print("Delivery request removed")
            if delopt==2:
                cur.execute("select * from delivery where agent_id="+str(agentId))
                deliHist=cur.fetchall()
                for ele in deliHist:
                    print("delivery ID: "+str(ele[0]))
                    print("Time: "+str(ele[1]))
                    print("Order ID: "+str(ele[4]))
            if delopt==3:
                cur.execute("select * from delivery where agent_id="+str(agentId)+" and delivery_status=0")
                pendingDel=cur.fetchall()
                for ele in pendingDel:
                    print("delivery ID: "+str(ele[0]))
                    print("Time: "+str(ele[1]))
                    print("Order ID: "+str(ele[4]))
                markopt=int(input("Select an delivery ID to mark as done (0 for skipping)"))
                if markopt!=0:
                    cur.execute("update delivery set delivery_status=1 where agent_id="+str(agentId)+" and delivery_id="+str(markopt))
                    print("Marked as done for delivery: "+str(markopt))

        else:
            print("Wrong credentials")
    print("Enter as:\n1.Customer   2.Admin   3.Retail Outlet   4.Delivery Agent   5.Exit")
    t=int(input())
    cur.close()
