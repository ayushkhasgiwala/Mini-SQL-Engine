import sqlparse
import sys

def colcheck(col, table_list,schema):
    for t in table_list:
        if col.lower() in schema[t]:
            return True
    return False

def print_table(nums, index_list, res_string):
    m=len(nums)
    if m==0:
        print(res_string)
        exit()
    n=len(nums[0])
    i,j,k=0,0,0
    x=len(index_list)
    while i<m:
        j=0
        while j<n:
            k=0
            while k<x:
                if j==index_list[k]:
                    res_string+=str(nums[i][j])
                    if(k!=x-1):
                        res_string+=" , "
                    else:
                        res_string+="\n"
                k+=1
            j+=1
        i+=1
    print(res_string)


#...........................project.........................
def project(nums, structure, column_list):
    #print(len(nums))
    if column_list[0]=="*":
        index_list=[]
        s=len(structure)
        i=0
        res_string=""
        while i<s:
            index_list.append(i)
            res_string+=structure[i]
            if(i!=s-1):
                res_string+=" , "
            else:
                res_string+="\n"
            i+=1
        #print(len(index_list))
        print_table(nums,index_list,res_string)
        exit()

    for cl in column_list:
        if cl  not in structure:
            print("The Column '",cl,"' Does Not Exist")
            exit()
    
    s=len(column_list)
    i=0
    index_list=[]
    res_string=""
    #print(s)
    while i<s:
        indx=structure.index(column_list[i])
        index_list.append(indx)
        res_string+=structure[indx]
        if(i!=s-1):
            res_string+=" , "
        else:
            res_string+="\n"
        i+=1
    print_table(nums,index_list,res_string)


def project2(finalresult,finalstruct):
    ans=""
    nm=len(finalstruct)
    i=0
    while i<nm:
        ans+=finalstruct[i]
        if i!=nm-1:
            ans+=" , "
        else:
            ans+="\n"
        i+=1
    n=len(finalresult)
    if n==0:
        print(ans)
        return
    m=len(finalresult[0])
    i,j=0,0
    while i<n:
        j=0
        while j<m:
            ans+=str(finalresult[i][j])
            if j!=m-1:
                ans+=" , "
            else:
                ans+="\n"
            j+=1
        i+=1
    print(ans)




#....................................aggregate function.............................
def aggregate(table_list,qry,stu,temp,schema):
    x=qry.find("(")
    q=qry[0:x]
    y=qry.find(")",x+1)
    col=qry[x+1:y].lower()
    #print(col)
    #temp=data[table_list[0]]
    if(q.upper()=="COUNT" and col=="*"):
        #print(len(temp))
        #exit()
        return len(temp)
    if(colcheck(col,table_list,schema)==False):
        print("The Column '",col,"' Does Not Exist")
        exit()
    cindex=stu.index(col)
    rowcount=len(temp)
    if(q.upper()=="MAX"):
        i=0
        res=[]
        while(i<rowcount):
            res.append(temp[i][cindex])
            i+=1
        ans=max(res)
        #print()
        #print(ans)
        return ans
        #exit()
    if(q.upper()=="MIN"):
        i=0
        res=[]
        while(i<rowcount):
            res.append(temp[i][cindex])
            i+=1
        ans=min(res)
        #print(ans)
        return ans
        #exit()
    if(q.upper()=="SUM"):
        i=0
        res=[]
        while(i<rowcount):
            res.append(temp[i][cindex])
            i+=1
        ans=sum(res)
        #print(ans)
        return ans
        #exit()
    if(q.upper()=="COUNT"):
        i=0
        res=[]
        while(i<rowcount):
            res.append(temp[i][cindex])
            i+=1
        ans=len(res)
        #print(ans)
        return ans
        #exit()
    if(q.upper()=="AVG"):
        i=0
        res=[]
        while(i<rowcount):
            res.append(temp[i][cindex])
            i+=1
        total=sum(res)
        count=len(res)
        if count!=0:
            ans=total/count
        else:
            ans=0
        #print(ans)
        return ans
        #exit()

#........................get conditions........................
def getconditions(q,schema):
    '''if ";" in q:
        x=len(q)
        q=q[0:x-1]
    else:
        x=len(q)
        if q[x-1]==" ":
            q=q[0:x-1]'''
    #print(q)
    x=len(q)
    q=q[0:x-1]
    #print(q)
    q=q.lower()
    q=q.replace(" = ","=")
    q=q.replace(" =","=")
    q=q.replace("= ","=")
    q=q.replace(" < ","<")
    q=q.replace(" <","<")
    q=q.replace("< ","<")
    q=q.replace(" > ",">")
    q=q.replace(" >",">")
    q=q.replace("> ",">")
    q=q.replace(" >= ",">=")
    q=q.replace(" >=",">=")
    q=q.replace(">= ",">=")
    q=q.replace(" <= ","<=")
    q=q.replace(" <=","<=")
    q=q.replace("<= ","<=")
    con=q.split(" ")
    #print(con)
    return con

def get_con_tokens(wc):
    if ">=" in wc:
        temp=wc.split(">=")
        c=">="
        return [temp[0],c,temp[1]]
    elif "<=" in wc:
        temp=wc.split("<=")
        c="<="
        return [temp[0],c,temp[1]]
    elif "<" in wc:
        temp=wc.split("<")
        c="<"
        return [temp[0],c,temp[1]]
    elif ">" in wc:
        temp=wc.split(">")
        c=">"
        return [temp[0],c,temp[1]]
    elif "=" in wc:
        temp=wc.split("=")
        c="="
        return [temp[0],c,temp[1]]

# ................................cartesian product.......................
def cartesianproduct(data, table_list,schema):
    s=len(table_list)
    i=1
    temp1=data[table_list[0]]
    ans=[]
    while i<s:
        m=len(temp1)
        temp2=data[table_list[i]][:]
        #print(temp2)
        n=len(temp2)
        j,k=0,0
        ans=[]
        while j<m:
            while k<n:
                p=temp1[j][:]
                #print(p)
                #print("....................")
                #print(temp1[j])
                #print("*****************")
                #print(data[table_list[i]][j])
                p.extend(temp2[k])
                ans.append(p)
                p=[]
                k+=1
            j+=1
            k=0
        i+=1
        j=0
        k=0
        temp1=[]
        temp1=ans[:]

    #................schema for cartesian product..........
    structure=[]
    i=0
    while i<s:
        structure.extend(schema[table_list[i]])
        i+=1
    #print(structure)
    #print(ans)
    return ans,structure

def ehelper(num2,condi,colmn,val,cindex):
    if(condi==">=" and num2[cindex]>=val):
        return True
    elif(condi=="<=" and num2[cindex]<=val):
        return True
    elif(condi=="<" and num2[cindex]<val):
        return True
    elif(condi==">" and num2[cindex]>val):
        return True
    elif(condi=="=" and num2[cindex]==val):
        return True
    return False


def evaluate_where(nums,cond,structure,op_flag):
    res=[]
    if op_flag==0:
        c=cond[0][0]
        cindex=structure.index(c)
        v=int(cond[0][2])
        s=len(nums)
        i=0
        while i<s:
            if(cond[0][1]==">=" and nums[i][cindex]>=v):
                res.append(nums[i])
            elif(cond[0][1]=="<=" and nums[i][cindex]<=v):
                res.append(nums[i])
            elif(cond[0][1]=="<" and nums[i][cindex]<v):
                res.append(nums[i])
            elif(cond[0][1]==">" and nums[i][cindex]>v):
                res.append(nums[i])
            elif(cond[0][1]=="=" and nums[i][cindex]==v):
                res.append(nums[i])
            i+=1

    else:
        c1=cond[0][0]
        c2=cond[1][0]
        cindex1=structure.index(c1)
        cindex2=structure.index(c2)
        v1=int(cond[0][2])
        v2=int(cond[1][2])
        s=len(nums)
        if(op_flag==1):
            i=0
            while i<s:
                if((ehelper(nums[i],cond[0][1],c1,v1,cindex1) and ehelper(nums[i],cond[1][1],c2,v2,cindex2)) == True):
                    res.append(nums[i])
                i+=1
        if(op_flag==2):
            i=0
            #print(s)
            while i<s:
                if((ehelper(nums[i],cond[0][1],c1,v1,cindex1) or ehelper(nums[i],cond[1][1],c2,v2,cindex2)) == True):
                    res.append(nums[i])
                i+=1
    return res


def getfinaltable(res,struct,column_list):
    finalres=[]
    temp=[]
    if column_list[0]=="*":
        finalres=res
        return res
    n=len(res)
    if n==0:
        return finalres
    #m=len(res[0])
    i=0
    #z=len(column_list)
    while i<n:
        for c in column_list:
            indx=struct.index(c)
            temp.append(res[i][indx])
        i+=1
        finalres.append(temp)
        temp=[]
    return finalres

                
def getfinalstruct(schema,table_list,cloumn_list,column_type):
    finalst=[]
    finalcol=[]
    if(column_list[0]=="*" and column_type[0]=="normal"):
        for t in table_list:
            tmp=[]
            tmp=schema[t]
            for k in tmp:
                st=""
                st=t+"."+k
                finalst.append(st)
                finalcol.append(k)
        return finalst,finalcol
    else:
        lnk=len(column_list)
        i=0
        while i<lnk:
            for t in table_list:
                if column_list[i] in schema[t] and column_type[i]=='normal':
                    st=""
                    st=t+"."+column_list[i]
                    #st=column_list[i]
                    finalst.append(st)
                    finalcol.append(column_list[i])
                    break
                elif column_list[i] in schema[t] and column_type[i]!='normal':
                    st=""
                    st+=column_type[i].lower()+"("+column_list[i]+")"
                    finalst.append(st)
                    finalcol.append(column_list[i])
                    break
                elif column_list[i]=="*" and column_type[i]!='normal': 
                    st=""
                    st+=column_type[i].lower()+"("+column_list[i]+")"
                    finalst.append(st)
                    finalcol.append(column_list[i])
                    break
            i+=1
        return finalst,finalcol


#..........................MAIN FUNCTION.........................................

#..........................getting the schema of the table.............................
m=open("./metadata.txt","r")
metadata=m.read()
l1=metadata.split("\n")
#print(metadata)
#print(l1)
x=len(l1)
#print(x)
schema={}
i=0
col=[]
while i<x:
    if(l1[i]=="<begin_table>"):
        flag=1
        i+=1
        tname=l1[i]
        tname=tname.lower()
        #i+=1

    elif(l1[i]=="<end_table>"):
        flag=0
        schema[tname]=col
        col=[]
        tname=""

    elif(flag==1):
        col.append(l1[i].lower())
    i+=1

#print(schema)
    
#.............................getting the data of the table in the map.....................
data={}
num1=[]
num2d=[]
for key in schema.keys():
    tname=key
    f=open("./"+tname+".csv")
    d=f.read()
    #print(len(d))
    #print(d)
    #print(d[0])
    x=0
    d=d.replace("\n",",")
    d+=","
    #print(d)
    k=len(d)
    #print(k)
    
    if d[0]!='"':
        n=d.find(",",x)
        l2=schema[tname]
        s=len(l2)
        i=0
        while x<k:
            if(i>=s):
                num2d.append(num1)
                num1=[]
                i=0
            n=d.find(",",x)
            num1.append(int(d[x:n]))
            #print(int(d[x:n]))
            #print(n)
            x=n+1
            i+=1
        #print(d[0])
        #print('............')
        num2d.append(num1)
        num1=[]
        data[tname]=num2d
        num2d=[]
    elif d[0]=='"':
        d=d[1:]
        #print(d)
        d=d.replace("\"","")
        #print(d)
        k=len(d)
        x=0
        n=d.find(",",x)
        #print(n)
        l2=schema[tname]
        s=len(l2)
        i=0
        while x<k:
            if(i>=s):
                num2d.append(num1)
                num1=[]
                i=0
            n=d.find(",",x)
            #print(int(d[x:n]))
            num1.append(int(d[x:n]))
            #print(int(d[x:n]))
            #print(n)
            x=n+1
            i+=1
        #print(d[0])
        #print('............')
        num2d.append(num1)
        num1=[]
        data[tname]=num2d
        num2d=[]


#print(data)

#................sql query input lelo..................
#s=input("Enter query :- ")
s=str(sys.argv[1])
#print(s)
##query="select max(col1), col2 from table1, table2,table3 where col1=4 AND col2=5;"
print("The input query is :- ",s)
print("\n")
print("The output is :- ")
print("................................................................................................................")
q=sqlparse.parse(s)
query=q[0]
#print(query) 
#print(query.tokens)
w=query.tokens
query_token=[]
#print(len(w))
sz=len(w)
i=0

for t in w:
    #print(str(t))
    if(str(t)!=" "):
        query_token.append(str(t))
    i+=1

#print(query_token)
s10=len(query_token)
#print(query_token[s10-1])
s11=len(query_token[s10-1])
if query_token[s10-1].endswith(";")==False:
    print("The query does not end with ';' therefore invalid query")
    exit()

ixz=len(query_token)
ind=0
while ind<ixz:
    if query_token[ind].lower()=="from":
        i=ind
    ind+=1
table_list=[]
tb=query_token[i+1]
tb=tb.replace(" ","")
tb=tb.lower()
table_list=tb.split(",")
#print(table_list)
for tl in table_list:
    if tl not in schema.keys():
        print("The Table - '",tl,"' Does not Exist")
        exit()

co=query_token[1]
distinct_flag,where_flag,group_flag,order_flag=0,0,0,0

column_list_temp=[]
column_list=[]
column_type=[]
if(co.upper()=="DISTINCT"):
    #print(1)
    cl=query_token[2]
    cl=cl.replace(" ","")
    cl=cl.lower()
    column_list_temp=cl.split(",")
    distinct_flag=1
else:
    cl=query_token[1]
    cl=cl.replace(" ","")
    cl=cl.lower()
    column_list_temp=cl.split(",")

#print(column_list_temp)
lnz=len(column_list_temp)
i=0
#print(lnz)
if lnz==1 and column_list_temp[0]=="*":
    column_list.append("*")
    column_type.append("normal")
else:
    while i<lnz:
        #print(i)
        if "MAX" in column_list_temp[i].upper() or "MIN" in column_list_temp[i].upper() or "SUM" in column_list_temp[i].upper() or "COUNT" in column_list_temp[i].upper() or "AVG" in column_list_temp[i].upper():
            qry=column_list_temp[i]
            x=qry.find("(")
            q=qry[0:x]
            y=qry.find(")",x+1)
            col=qry[x+1:y]
            column_list.append(col)
            column_type.append(q.upper())
        else:
            column_list.append(column_list_temp[i])
            column_type.append("normal")
        i+=1
    i=0
    while i<lnz:
        if column_list[i]=="*" and column_type[i].upper()=="COUNT":
            i+=1
            continue
        else:
            if(colcheck(column_list[i],table_list,schema)==False):
                #print(2)
                print("The Column - '",column_list[i],"' does not exist")
                exit()
            i+=1

#print(column_list)
#print(column_type)


for qt in query_token:
    if "WHERE" in qt.upper():
        where_flag=1
    if "GROUP BY" in qt.upper():
        group_flag=1
    if "ORDER BY" in qt.upper():
        order_flag=1

#print(2)

'''if "MAX" in co.upper() or "MIN" in co.upper() or "SUM" in co.upper() or "COUNT" in co.upper() or "AVG" in co.upper():
    aggregate(table_list,query_token[1],schema,data)'''
#..............................................pure aggregate queries.............................................
iz=len(column_list)
if iz==1 and column_type[0]!="normal":
    #print(2)
    if "MAX" in column_list_temp[0].upper() or "MIN" in column_list_temp[0].upper() or "SUM" in column_list_temp[0].upper() or "COUNT" in column_list_temp[0].upper() or "AVG" in column_list_temp[0].upper():
        
        '''if column_type[0].upper()=="COUNT":
            if column_list[0]=="*":
                column_list[0]=schema[table_list[0]][0]'''
        
        
        if where_flag==0 and group_flag==0:
            if len(table_list)==1:
                #print(1)
                a=aggregate(table_list,column_list_temp[0],schema[table_list[0]],data[table_list[0]],schema)
                print(column_list_temp[0])
                print(a)
                exit()
            else:
                ans,structure=cartesianproduct(data,table_list,schema)
                a=aggregate(table_list,column_list_temp[0],structure,ans,schema)
                print(column_list_temp[0])
                print(a)
                exit()
            
        
        #and order_flag==0 and distinct_flag==0
        elif where_flag==1 and group_flag==0:
            q=""
            for qt in query_token:
                if qt.upper().startswith("WHERE") == True:
                    q=qt
            con=getconditions(q,schema)
            op_flag=0
            for c in con:
                if c.upper()=="AND":
                    op_flag=1
                if c.upper()=="OR":
                    op_flag=2

            if op_flag==1 or op_flag==2:
                l1=get_con_tokens(con[1])
                l2=get_con_tokens(con[3])
                if colcheck(l1[0],table_list,schema) == False:
                    print("The Column '",l1[0],"' Does Not Exist")
                    exit()
                if colcheck(l2[0],table_list,schema) == False:
                    print("The Column '",l2[0],"' Does Not Exist")
                    exit()
                l=[]
                l.append(l1)
                l.append(l2)
                if len(table_list) == 1:
                    res=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
                    structure=schema[table_list[0]]
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    a=aggregate(table_list,column_list_temp[0],structure,res,schema)
                    print(column_list_temp[0])
                    print(a)
                    exit()
                else:
                    ans,structure=cartesianproduct(data,table_list,schema)
                    res=evaluate_where(ans,l,structure,op_flag)
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    a=aggregate(table_list,column_list_temp[0],structure,res,schema)
                    print(column_list_temp[0])
                    print(a)
                    exit()
            else:
                l1=get_con_tokens(con[1])
                if colcheck(l1[0],table_list,schema) == False:
                    print("The Column '",l1[0],"' Does Not Exist")
                    exit()
                l=[]
                l.append(l1)
                #print(l)
                if len(table_list) == 1:
                    res=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
                    structure=schema[table_list[0]]
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    a=aggregate(table_list,column_list_temp[0],structure,res,schema)
                    print(column_list_temp[0])
                    print(a)
                    exit()
                else:
                    ans,structure=cartesianproduct(data,table_list,schema)
                    res=evaluate_where(ans,l,structure,op_flag)
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    a=aggregate(table_list,column_list_temp[0],structure,res,schema)
                    print(column_list_temp[0])
                    print(a)
                    exit()
                
        '''elif distinct_flag==1 and where_flag==0 and group_flag==0:
            res_tp=[]
            if len(table_list)==1:
                fr=data[table_list[0]][:]
                stm=schema[table_list[0]]
            else:
                fr,stm=cartesianproduct(data,table_list,schema)
            
            if column_list[0]=="*":
                kj=len(fr)
                i=0
                #print(fr)
                while i<kj:
                    if fr[i] not in res_tp:
                        #print(fr[i])
                        res_tp.append(fr[i])
                    i+=1
                if column_type[0].upper()=="COUNT":
                    print("count(*)")
                    print(len(res_tp))
                    exit()
            else:
                cm=column_list[0]
                idfx=stm.index(cm)
                kj=len(fr)
                i=0
                #print(fr)
                while i<kj:
                    if fr[i][idfx] not in res_tp:
                        #print(fr[i])
                        res_tp.append(fr[i][idfx])
                    i+=1
                if column_type[0].upper()=="MAX":
                    print("max(",column_list[0],")")
                    print(max(res_tp))
                    exit()
                if column_type[0].upper()=="MIN":
                    print("min(",column_list[0],")")
                    print(min(res_tp))
                    exit()
                if column_type[0].upper()=="SUM":
                    print("sum(",column_list[0],")")
                    print(sum(res_tp))
                    exit()
                if column_type[0].upper()=="COUNT":
                    print("count(",column_list[0],")")
                    print(len(res_tp))
                    exit()
                if column_type[0].upper()=="AVG":
                    print("avg(",column_list[0],")")
                    print(sum(res_tp)/len(res_tp))
                    exit()'''
        
        '''elif where_flag==1 and distinct_flag==1 and group_flag==0:
            q=""
            for qt in query_token:
                if qt.upper().startswith("WHERE") == True:
                    q=qt
            con=getconditions(q,schema)
            op_flag=0
            for c in con:
                if c.upper()=="AND":
                    op_flag=1
                if c.upper()=="OR":
                    op_flag=2

            if op_flag==1 or op_flag==2:
                l1=get_con_tokens(con[1])
                l2=get_con_tokens(con[3])
                if colcheck(l1[0],table_list,schema) == False:
                    print("The Column '",l1[0],"' Does Not Exist")
                    exit()
                if colcheck(l2[0],table_list,schema) == False:
                    print("The Column '",l2[0],"' Does Not Exist")
                    exit()
                l=[]
                l.append(l1)
                l.append(l2)
                if len(table_list) == 1:
                    res=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
                    structure=schema[table_list[0]]
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
                else:
                    ans,structure=cartesianproduct(data,table_list,schema)
                    res=evaluate_where(ans,l,structure,op_flag)
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
            else:
                l1=get_con_tokens(con[1])
                if colcheck(l1[0],table_list,schema) == False:
                    print("The Column '",l1[0],"' Does Not Exist")
                    exit()
                l=[]
                l.append(l1)
                print(l)
                if len(table_list) == 1:
                    res=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
                    structure=schema[table_list[0]]
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
                else:
                    ans,structure=cartesianproduct(data,table_list,schema)
                    res=evaluate_where(ans,l,structure,op_flag)
                    if len(res)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
            res_tp=[]
            if column_list[0]=="*":
                kj=len(res)
                i=0
                #print(fr)
                while i<kj:
                    if res[i] not in res_tp:
                        #print(fr[i])
                        res_tp.append(res[i])
                    i+=1
                if column_type[0].upper()=="COUNT":
                    print("count(*)")
                    print(len(res_tp))
                    exit()
            else:
                cm=column_list[0]
                idfx=structure.index(cm)
                kj=len(fr)
                i=0
                #print(fr)
                while i<kj:
                    if res[i][idfx] not in res_tp:
                        #print(fr[i])
                        res_tp.append(res[i][idfx])
                    i+=1
                if column_type[0].upper()=="MAX":
                    print("max(",column_list[0],")")
                    print(max(res_tp))
                    exit()
                if column_type[0].upper()=="MIN":
                    print("min(",column_list[0],")")
                    print(min(res_tp))
                    exit()
                if column_type[0].upper()=="SUM":
                    print("sum(",column_list[0],")")
                    print(sum(res_tp))
                    exit()
                if column_type[0].upper()=="COUNT":
                    print("count(",column_list[0],")")
                    print(len(res_tp))
                    exit()
                if column_type[0].upper()=="AVG":
                    print("avg(",column_list[0],")")
                    print(sum(res_tp)/len(res_tp))
                    exit()'''
        '''elif group_flag==0 and (where_flag==1 or order_flag==1 or distinct_flag==1):
            print("Invalid Query")
            exit()'''
elif iz>1:
    i=0
    dp_flag=0
    f1=0
    f2=0
    tops=""
    while i<iz:
        if column_type[i]=="normal":
            f1=1
            tops=column_list[i]
        if column_type[i]!="normal":
            f2=1
        i+=1
    if f1==1 and f2==1: 
        if group_flag==0:
            print("Invalid query")
            exit()
        '''else:
            i=0
            while i<iz:
                if column_type[i]!="normal":
                    if column_list[i]=="*":
                        column_list[i]=tops
                i+=1'''
    if f2==1 and f1==0:
        '''i=0
        while i<iz:
            if column_type[i]!="normal":
                if column_list[i]=="*":
                    column_list[i]=schema[table_list[0]][0]
            i+=1'''
        fr=[]
        stm=[]
        if len(table_list)==1:
            fr=data[table_list[0]][:]
            stm=schema[table_list[0]]
        else:
            fr,stm=cartesianproduct(data,table_list,schema)
        
        if where_flag==1 and group_flag==0:
            fr=[]
            stm=[]
            q=""
            for qt in query_token:
                if qt.upper().startswith("WHERE") == True:
                    q=qt
            con=getconditions(q,schema)
            op_flag=0
            for c in con:
                if c.upper()=="AND":
                    op_flag=1
                if c.upper()=="OR":
                    op_flag=2

            if op_flag==1 or op_flag==2:
                l1=get_con_tokens(con[1])
                l2=get_con_tokens(con[3])
                if colcheck(l1[0],table_list,schema) == False:
                    print("The Column '",l1[0],"' Does Not Exist")
                    exit()
                if colcheck(l2[0],table_list,schema) == False:
                    print("The Column '",l2[0],"' Does Not Exist")
                    exit()
                l=[]
                l.append(l1)
                l.append(l2)
                if len(table_list) == 1:
                    fr=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
                    stm=schema[table_list[0]]
                    if len(fr)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
                else:
                    ans,stm=cartesianproduct(data,table_list,schema)
                    fr=evaluate_where(ans,l,stm,op_flag)
                    if len(fr)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
            else:
                l1=get_con_tokens(con[1])
                if colcheck(l1[0],table_list,schema) == False:
                    print("The Column '",l1[0],"' Does Not Exist")
                    exit()
                l=[]
                l.append(l1)
                #print(l)
                if len(table_list) == 1:
                    fr=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
                    stm=schema[table_list[0]]
                    if len(fr)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
                else:
                    ans,stm=cartesianproduct(data,table_list,schema)
                    fr=evaluate_where(ans,l,stm,op_flag)
                    if len(fr)==0:
                        print("Zero rows selected")
                        exit()
                    #aggregate(table_list,query_token[1],schema,res)
        
        '''if distinct_flag==1 and group_flag==0:
            j=0
            dp_flag=1
            temp_ans_list=[]
            while j<iz:
                res_tp=[]
                if column_list[j]=="*":
                    kj=len(fr)
                    i=0
                    #print(fr)
                    while i<kj:
                        if fr[i] not in res_tp:
                            #print(fr[i])
                            res_tp.append(fr[i])
                        i+=1
                    #print(res_tp)
                    if column_type[j].upper()=="COUNT":
                        #print("count(*)")
                        #print(len(res_tp))
                        #exit()
                        temp_ans_list.append(len(res_tp))
                else:
                    cm=column_list[j]
                    idfx=stm.index(cm)
                    kj=len(fr)
                    i=0
                    #print(fr)
                    while i<kj:
                        if fr[i][idfx] not in res_tp:
                            #print(fr[i])
                            res_tp.append(fr[i][idfx])
                        i+=1
                    #print(res_tp)
                    if column_type[j].upper()=="MAX":
                        #print("max(",column_list[0],")")
                        #print(max(res_tp))
                        #exit()
                        temp_ans_list.append(max(res_tp))
                    if column_type[j].upper()=="MIN":
                        #print("min(",column_list[0],")")
                        #print(min(res_tp))
                        #exit()
                        temp_ans_list.append(min(res_tp))
                    if column_type[j].upper()=="SUM":
                        #print("sum(",column_list[0],")")
                        #print(sum(res_tp))
                        #exit()
                        temp_ans_list.append(sum(res_tp))
                    if column_type[j].upper()=="COUNT":
                        #print("count(",column_list[0],")")
                        #print(len(res_tp))
                        #exit()
                        temp_ans_list.append(len(res_tp))
                    if column_type[j].upper()=="AVG":
                        #print("avg(",column_list[0],")")
                        #print(sum(res_tp)/len(res_tp))
                        #exit()
                        temp_ans_list.append(sum(res_tp)/len(res_tp))
                j+=1

            i=0
            s=""
            while i<iz:
                s+=column_list_temp[i]
                if i!=iz-1:
                    s+=" , "
                i+=1
            print(s)
            sa=""
            i=0
            while i<iz:
                sa+=str(temp_ans_list[i])
                if i!=iz-1:
                    sa+=" , "
                i+=1
            print(sa)
            #print(temp_ans_list)
            exit()'''

        if dp_flag==0 and group_flag==0:
            i=0
            temp_ans_list=[]
            #print("...................")
            #print(fr)
            while i<iz:
                a=aggregate(table_list,column_list_temp[i],stm,fr,schema)
                #print(a)
                temp_ans_list.append(a)
                i+=1
            i=0
            s=""
            while i<iz:
                s+=column_list_temp[i]
                if i!=iz-1:
                    s+=" , "
                i+=1
            print(s)
            sa=""
            i=0
            while i<iz:
                sa+=str(temp_ans_list[i])
                if i!=iz-1:
                    sa+=" , "
                i+=1
            print(sa)
            #print(temp_ans_list)
            exit()

        
            


#...................................................................................................................


res=[]
structure=[]
finalresult=[]
finalstruct=[]
finalcol=[]
finalstruct,finalcol=getfinalstruct(schema,table_list,column_list,column_type)
#print(finalstruct)

i=0
while i<iz:
    if column_type[i]!="normal":
        #print("890")
        if column_list[i]=="*":
            column_list[i]=schema[table_list[0]][0]
    i+=1
#print(column_list)
#..........................................where clause.....................................
if where_flag==1:
    q=""
    for qt in query_token:
        if qt.upper().startswith("WHERE") == True:
            q=qt
    con=getconditions(q,schema)
    op_flag=0
    for c in con:
        if c.upper()=="AND":
            op_flag=1
        if c.upper()=="OR":
            op_flag=2

    if op_flag==1 or op_flag==2:
        l1=get_con_tokens(con[1])
        l2=get_con_tokens(con[3])
        if colcheck(l1[0],table_list,schema) == False:
            print("The Column '",l1[0],"' Does Not Exist")
            exit()
        if colcheck(l2[0],table_list,schema) == False:
            print("The Column '",l2[0],"' Does Not Exist")
            exit()
        l=[]
        l.append(l1)
        l.append(l2)
        if len(table_list) == 1:
            res=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
            finalresult=getfinaltable(res, schema[table_list[0]], column_list)
            #print(finalresult)
            structure=schema[table_list[0]]
            #print(res)
            #project(res,schema[table_list[0]],column_list)
            #project(finalresult,schema[table_list[0]],column_list,finalstruct)
            #print(res)
        else:
            ans,structure=cartesianproduct(data,table_list,schema)
            res=evaluate_where(ans,l,structure,op_flag)
            finalresult=getfinaltable(res, structure, column_list)
            #print(finalresult)
            #project(res,structure,column_list)
            #print(res)
    else:
        l1=get_con_tokens(con[1])
        if colcheck(l1[0],table_list,schema) == False:
            print("The Column '",l1[0],"' Does Not Exist")
            exit()
        l=[]
        l.append(l1)
        #print(l)
        if len(table_list) == 1:
            res=evaluate_where(data[table_list[0]],l,schema[table_list[0]],op_flag)
            finalresult=getfinaltable(res, schema[table_list[0]], column_list)
            #print(finalresult)
            structure=schema[table_list[0]]
            #project(res,schema[table_list[0]],column_list)
            #print(res)
        else:
            ans,structure=cartesianproduct(data,table_list,schema)
            res=evaluate_where(ans,l,structure,op_flag)
            finalresult=getfinaltable(res, structure, column_list)
            #print(finalresult)
            #project(res,structure,column_list)
            #print(res)
    if len(finalresult)==0:
        print("No rows selected")
        exit()
    if distinct_flag==0 and order_flag==0 and group_flag==0:
           project2(finalresult,finalstruct)
           exit()

else:
    if len(table_list)==1:
        temp_res=data[table_list[0]]
        structure=schema[table_list[0]]
        finalresult=getfinaltable(temp_res, structure, column_list)
        res=data[table_list[0]][:]
    else:
        temp_res,structure=cartesianproduct(data,table_list,schema)
        finalresult=getfinaltable(temp_res, structure, column_list)
        res=temp_res[:]

#............................................only select query....................................
if where_flag==0 and order_flag==0 and distinct_flag==0 and group_flag==0:
    project2(finalresult,finalstruct)
    exit()

#..................................................group by.................................
if group_flag==1:
    dz=len(query_token)
    i,indx=0,0
    while i<dz:
        if query_token[i].upper() == "GROUP BY":
            indx=i
            break
        i+=1
    group_col=query_token[indx+1].lower()
    #print(group_col)
    lmk=len(column_list)
    i=0
    while i<lmk:
        if column_type[i]=="normal" and column_list[i]!=group_col:
            print("Error - Invalid group query")
            exit()
        i+=1
    grp_col_indx=structure.index(group_col)
    #print(grp_col_indx)
    final_dict={}
    i=0
    while i<lmk:
        if column_type[i]!="normal":
            temp_dict={}
            ctemp=column_list[i]
            ctemp_indx=structure.index(ctemp)
            rs=len(res)
            j=0
            while j<rs:
                if res[j][grp_col_indx] not in temp_dict.keys():
                    temp_dict[res[j][grp_col_indx]]=[]
                temp_dict[res[j][grp_col_indx]].append(res[j][ctemp_indx])
                j+=1
            #print(temp_dict)
            for key in temp_dict.keys():
                if column_type[i].upper()=="MAX":
                    ans=max(temp_dict[key])
                elif column_type[i].upper()=="MIN":
                    ans=min(temp_dict[key])
                elif column_type[i].upper()=="SUM":
                    ans=sum(temp_dict[key])
                elif column_type[i].upper()=="COUNT":
                    ans=len(temp_dict[key])
                elif column_type[i].upper()=="AVG":
                    sumz=sum(temp_dict[key])
                    count=len(temp_dict[key])
                    ans=sumz/count
                if key not in final_dict.keys():
                    final_dict[key]=[]
                final_dict[key].append(ans)
        i+=1
    #print(final_dict)
    temp_res=[]
    i=0
    for key in final_dict.keys():
        r=[]
        tp=final_dict[key]
        kj=len(tp)
        k=0
        i=0
        while i<lmk:
            if column_type[i]=="normal":
                r.append(key)
            else:
                if k<kj:
                    r.append(tp[k])
                k+=1
            i+=1
        temp_res.append(r)
    
    #print(temp_res)
    finalresult=temp_res
    #print(temp_dict)
    if where_flag==0 and order_flag==0 and distinct_flag==0:
        project2(finalresult,finalstruct)
        exit()

#........................................distinct ...............................................
if distinct_flag==1:
    res_temp=[]
    n=len(finalresult)
    if n==0:
        for cl in column_list:
            if cl  not in structure:
                print("The Column '",cl,"' Does Not Exist")
                exit()
        s=len(finalstruct)
        ans=""
        i=0
        while i<s:
            ans+=finalstruct[i]
            if (i!=s-1):
                ans+=" , "
            else:
                ans+="\n"
            i+=1
        print(ans)
        exit()
    #m=len(res[0])
    i=0
    #print(res)
    while i<n:
        if finalresult[i] not in res_temp:
            #print(res[i])
            res_temp.append(finalresult[i])
        i+=1
    finalresult=res_temp
    #project2(finalresult,finalstruct)
    #res=res_temp
    #project(res,structure,column_list)
    if order_flag==0 and group_flag==0 and where_flag==0:
        project2(finalresult,finalstruct)
        exit()

#......................................................order by................................................
if order_flag==1:
    dz=len(query_token)
    i,indx=0,0
    while i<dz:
        if query_token[i].upper() == "ORDER BY":
            indx=i
            break
        i+=1
    tp=query_token[indx+1].lower()
    tl=tp.split(" ")
    order_col=tl[0].lower()
    if len(tl)==1:
        order_type="ASC"
    else:
        order_type=tl[1].upper()
    #print(order_col)
    #print(column_list)
    if distinct_flag==1:
        #or column_list[0]!="*"
        if order_col not in column_list and column_list[0]!="*":
            print("Error: In case of Distinct and orderby, we cannot order on the col which is not in the selected column")
            exit()
    #or column_list[0]=="*"
    if order_col in column_list or column_list[0]=="*":
        #print(123)
        #print(finalstruct)
        indx=finalcol.index(order_col)
        #print(indx)
        #print(finalresult)
        if order_type=="ASC":
            #print(678)
            finalresult.sort(key = lambda x:x[indx])
        elif order_type=="DESC":
            #print("yubyun")
            finalresult.sort(key = lambda x:x[indx], reverse=True)
    else:
        indx=structure.index(order_col)
        #print(indx)
        #print(res)
        if order_type=="ASC":
            res.sort(key = lambda x:x[indx])
        elif order_type=="DESC":
            res.sort(key = lambda x:x[indx], reverse=True)
        finalresult=getfinaltable(res,structure,column_list)

    if where_flag==0 and distinct_flag==0 and group_flag==0:
        project2(finalresult,finalstruct)
        exit()


project2(finalresult,finalstruct)
    
    
