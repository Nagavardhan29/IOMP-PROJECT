from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider
import os
from django.core.files.storage import FileSystemStorage
import pickle

global details, username
details=''
global contract, product_name


def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Drug.json' #Drug contract code
    deployed_contract_address = '0xCE729A28EaD000ea6C7AE68D178508A636b59CC7' #hash address to access Drug contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call()
    if contract_type == 'addproduct':
        details = contract.functions.getTracingData().call()    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Drug.json' #Drug contract file
    deployed_contract_address = '0xCE729A28EaD000ea6C7AE68D178508A636b59CC7' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'addproduct':
        details+=currentData
        msg = contract.functions.setTracingData(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    

def updateQuantityBlock(currentData):
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Drug.json' #student contract file
    deployed_contract_address = '0xCE729A28EaD000ea6C7AE68D178508A636b59CC7' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.setTracingData(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    
def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})
    
def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def AddProduct(request):
    if request.method == 'GET':
       return render(request, 'AddProduct.html', {})

def UpdateTracingAction(request):
    if request.method == 'GET':
        global product_name
        product_name = request.GET['pname']
        output = '<tr><td><font size="" color="black">Product&nbsp;Name</font></td>'
        output += '<td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value='+product_name+' readonly/></td></tr>'
        context= {'data':output}
        return render(request, 'AddTracing.html', context)    

def UpdateTracing(request):
    if request.method == 'GET':
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Drug Name</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Image</font></th>'
        output+='<th><font size=3 color=black>Last Update Date</font></th>'
        output+='<th><font size=3 color=black>Current Tracing Info</font></th>'
        output+='<th><font size=3 color=black>Update New Tracing Info</font></th></tr>'
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'addproduct':
                output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                output+='<td><img src="/static/products/'+arr[5]+'" width="200" height="200"></img></td>'
                output+='<td><font size=3 color=black>'+str(arr[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td>'
                output+='<td><a href=\'UpdateTracingAction?pname='+arr[1]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'                    
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'UpdateTracing.html', context)              
        
    
def AddTracingAction(request):
    if request.method == 'POST':
        product_name = request.POST.get('t1', False)
        tracing_type = request.POST.get('t2', False)
        tracing_status = request.POST.get('t3', False)
        index = 0
        record = ''
        readDetails("addproduct")
        rows = details.split("\n")
        tot_qty = 0
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct":
                if arr[1] == product_name:
                    today = date.today()
                    index = i
                    record = arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+arr[4]+"#"+arr[5]+"#"+str(today)+"#"+tracing_type+"! "+tracing_status+"\n"
                    break
        for i in range(len(rows)-1):
            if i != index:
                record += rows[i]+"\n"
        updateQuantityBlock(record)
        context= {'data':"Tracing details updated"}
        return render(request, 'AdminScreen.html', context)
          
def AddProductAction(request):
    if request.method == 'POST':
        cname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        image = request.FILES['t5']
        imagename = request.FILES['t5'].name

        today = date.today()
        fs = FileSystemStorage()
        filename = fs.save('DrugTraceApp/static/products/'+imagename, image)
        
        data = "addproduct#"+cname+"#"+price+"#"+qty+"#"+desc+"#"+imagename+"#"+str(today)+"#Production State\n"
        saveDataBlockChain(data,"addproduct")
        context= {'data':"Product details saved in Blockchain"}
        return render(request, 'AddProduct.html', context)
        
   
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        record = 'none'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username:
                    record = "exists"
                    break
        if record == 'none':
            data = "signup#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"signup")
            context= {'data':'Signup process completd and record saved in Blockchain'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Register.html', context)    



def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = "Login.html"
        context= {'data':'Invalid login details'}
        if username == 'admin' and password == 'admin':
            context = {'data':"Welcome "+username}
            status = "AdminScreen.html"
        else:
            readDetails("signup")
            rows = details.split("\n")
            for i in range(len(rows)-1):
                arr = rows[i].split("#")
                if arr[0] == "signup":
                    if arr[1] == username and arr[2] == password:
                        context = {'data':"Welcome "+username}
                        status = 'UserScreen.html'
                        file = open('session.txt','w')
                        file.write(username)
                        file.close()
                        break
        return render(request, status, context)              


def ViewTracing(request):
    if request.method == 'GET':
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Drug Name</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Image</font></th>'
        output+='<th><font size=3 color=black>Last Update Date</font></th>'
        output+='<th><font size=3 color=black>Current Tracing Info</font></th></tr>'
        
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'addproduct':
                output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                output+='<td><img src="/static/products/'+arr[5]+'" width="200" height="200"></img></td>'
                output+='<td><font size=3 color=black>'+str(arr[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td>'                             
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ViewTracing.html', context)   
        
            
