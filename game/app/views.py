from django.shortcuts import render, redirect
from app.models import User
from app.models import GameServer


from django.db.models import Q


from django.db.models import F
from random import randint

# Create your views here.


def Dashboard(request):

    return render(request, 'dashboard.html' )


def Demo(request):

    return render(request, 'demo.html' )
    



from django.http import JsonResponse
 

def get_value(request):
    value = GameServer.objects.get(id=request.session['GameServerId']).change  # Adjust the query as per your model and field
    return JsonResponse({'value': value})



def player_reload(request):
    value = User.objects.get(id=request.session['LoginID']).change  # Adjust the query as per your model and field
    return JsonResponse({'value': value})



def Home(request):
    if request.method=="POST":

    

        username1= request.POST.get('username')
        password1= request.POST.get('password')
        
         
        loginV = User.objects.filter(Q(username = username1) & Q(password = password1))
        
        if loginV.exists():
                 user = loginV[0]
                # Access the user's id
                 user_id = user.id
                 request.session['LoginID'] =user_id
                 User.objects.filter(pk=request.session['LoginID']).update(status='online' )
                 LoginId= request.session['LoginID']
                 return redirect('Login')

                  
        else:
                # Handle the case when no user is found
                error_message1 = "User not found"
                return render(request, 'index.html', {'error_message1': error_message1})

    view=User.objects.all()

        
    return render(request, 'index.html',{'view':view})
    



    
    
#---------------------------------------------------------------------------------------------------------------------------------- 

# Create your views here.
def register(request):
    if request.method=="POST":
        name= request.POST.get('name')
        username= request.POST.get('username')
        mail= request.POST.get('mail')
        number= request.POST.get('number')
        pas= request.POST.get('pass')
 
        try:
            obj=User(name=name,username=username , email=mail , phone=number , password=pas ,status="offline",change=0,emoji=1)
            obj.save()
            return redirect('home')
        except Exception as e:
               error_message = "choose another user id this user is is already taken"
               return render(request, 'registration.html', {'error_message': error_message})
    view=User.objects.all()

    return render(request, 'registration.html',{'view':view})







#---------------------------------------------------------------------------------------------------------------------------------- 

# Create your views here.
def Login(request):
    LoginId= request.session['LoginID']
    user = User.objects.get(id=request.session['LoginID'])
    view=User.objects.all()
    requests=GameServer.objects.all()


    User.objects.update(change=randint(0, 10000)) 


    #num = User.objects.get(id=request.session['LoginID'])
    #num1=num.change+1
    #User.objects.filter(pk=request.session['LoginID']).update(change= num1 )
    
    return render(request, 'login.html', {'user': user, 'view': view, 'requests': requests ,'LoginId':LoginId})

        






def RegisterServer(request,id):
        LoginId= request.session['LoginID']
        

        player1 = User.objects.get(id=request.session['LoginID'])
        player2 = User.objects.get(id=id)

        print(f"player 1 id : {player1.id}")
        print(f"player 2 id : {player2.id}")
        

        createnewServer = GameServer.objects.filter(Q(player1 = player1.id) & Q(player2 = player2.id))

        if createnewServer.exists():
                    error_message1 = "aleredy request sent "
                            
                    user = User.objects.get(id=request.session['LoginID'])
                    view=User.objects.all()
                    requests=GameServer.objects.all()
 


                    return render(request, 'login.html', {'user': user, 'view': view, 'requests': requests ,'LoginId':LoginId,'error_message1': error_message1})
                              

        else:
                 #here we are registerin in game server
                obj1=GameServer(player1=player1.id,player2=player2.id , ans_player1="" , ans_player2="", winner="" ,player1Win=0,player2Win=0,status="waiting",cnt=0,player1_click=0,player2_click=0,change=0,player1name=player1.username,player2name=player2.username,emoji=1,emoji2=1)
                obj1.save()


                num = User.objects.get(id=player1.id)
                num1=num.change+1
                User.objects.filter(pk=player1.id).update(change =  num1)


                num = User.objects.get(id=player2.id)
                num1=num.change+1
                User.objects.filter(pk=player2.id).update(change =  num1)





                return redirect(Login)
                
        

                


#---------------------------------------------------------------------------------------------------------------------------------- 


def GamePage_accept(request,id):
    
    request.session['GameServerId'] =id
    request.session['Player'] ='Player2'
    GameServer.objects.filter(pk=id).update(status='start' )

    Other_Player_Id = GameServer.objects.get(id=request.session['GameServerId']).player1

    request.session['Other_Player_Id'] = Other_Player_Id

    
    num = User.objects.get(id=request.session['Other_Player_Id'])
    num1=num.change+1
    User.objects.filter(pk=request.session['Other_Player_Id']).update(change =  num1)




    return redirect(GamePage)

    


def GamePage_sender(request,id):
    request.session['GameServerId'] =id
    request.session['Player'] ='Player1'

    Other_Player_Id = GameServer.objects.get(id=request.session['GameServerId']).player2

    request.session['Other_Player_Id'] = Other_Player_Id

    GameServer.objects.filter(pk=id).update(status='start' )


    num = User.objects.get(id=request.session['Other_Player_Id'])
    num1=num.change+1
    User.objects.filter(pk=request.session['Other_Player_Id']).update(change =  num1)



    return redirect(GamePage)

    




#---------------------------------------------------------------------------------------------------------------------------------- 

def GamePage(request):



    allGame=GameServer.objects.all()
    #cnt = GameServer.objects.get(id=request.session['GameServerId'])

     
    return render(request, 'game.html', {'GameServerId': request.session['GameServerId'], 'Player': request.session['Player'], 'allGame': allGame  } )
    





#---------------------------------------------------------------------------------------------------------------------------------- 
 
 
def GamePage_sender_stone(request,value,id):
    cnt = GameServer.objects.get(id=id)

    
     


    if request.session['Player'] == "Player1":
          if cnt.cnt==0:
                
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )



                GameServer.objects.filter(pk=id).update(ans_player2="" )
                GameServer.objects.filter(pk=id).update(ans_player1=value )

                GameServer.objects.filter(pk=id).update(cnt=1 )

                player1 = GameServer.objects.get(id=id)
                GameServer.objects.filter(pk=id).update(player1_click= 1 )

                

                

                 
                

                if player1.player1_click ==1 and player1.player1_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )

                        
                      



                
                

          if cnt.cnt==1:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )



                GameServer.objects.filter(pk=id).update(ans_player1=value )
                GameServer.objects.filter(pk=id).update(cnt=0 )

                GameServer.objects.filter(pk=id).update(player1_click=1 )


                player1 = GameServer.objects.get(id=id)


                

                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )


# ------------------- score update 
                if player1.ans_player1 =="stone" and player1.ans_player2=="sesores":
                    GameServer.objects.filter(pk=id).update(player1Win =  player1.player1Win+1)
                
                
                if player1.ans_player1 =="stone" and player1.ans_player2=="paper":
                    GameServer.objects.filter(pk=id).update(player2Win =  player1.player2Win+1)
                     

          
          
          
    if request.session['Player'] == "Player2":
          if cnt.cnt==0:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )

                GameServer.objects.filter(pk=id).update(ans_player1="" )
                GameServer.objects.filter(pk=id).update(ans_player2=value )
                
                GameServer.objects.filter(pk=id).update(cnt=1 )

                 

                
                GameServer.objects.filter(pk=id).update(player2_click=1 )
                player1 = GameServer.objects.get(id=id)
                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )

                        


          if cnt.cnt==1:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )

                GameServer.objects.filter(pk=id).update(ans_player2=value )
                GameServer.objects.filter(pk=id).update(cnt=0 )

                
                GameServer.objects.filter(pk=id).update(player2_click=1 )
                player1 = GameServer.objects.get(id=id)
                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )




# ------------------- score update 

                if player1.ans_player2 =="stone" and player1.ans_player1=="sesores":
                    GameServer.objects.filter(pk=id).update(player2Win =  player1.player2Win+1)
                
                
                if player1.ans_player2 =="stone" and player1.ans_player1=="paper":
                    GameServer.objects.filter(pk=id).update(player1Win =  player1.player1Win+1)
                     
   



    return redirect(GamePage)













#---------------------------------------------------------------------------------------------------------------------------------- 
def GamePage_sender_paper(request,value,id):
    cnt = GameServer.objects.get(id=id)

    
     


    if request.session['Player'] == "Player1":
          if cnt.cnt==0:
                
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )



                GameServer.objects.filter(pk=id).update(ans_player2="" )
                GameServer.objects.filter(pk=id).update(ans_player1=value )

                GameServer.objects.filter(pk=id).update(cnt=1 )

                player1 = GameServer.objects.get(id=id)
                GameServer.objects.filter(pk=id).update(player1_click= 1 )

                

                

                 
                

                if player1.player1_click ==1 and player1.player1_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )

                        
                      



                
                

          if cnt.cnt==1:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )



                GameServer.objects.filter(pk=id).update(ans_player1=value )
                GameServer.objects.filter(pk=id).update(cnt=0 )

                GameServer.objects.filter(pk=id).update(player1_click=1 )


                player1 = GameServer.objects.get(id=id)


                

                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )
                


# ------------------- score update 
                if player1.ans_player1 =="paper" and player1.ans_player2=="stone":
                    GameServer.objects.filter(pk=id).update(player1Win =  player1.player1Win+1)
                     
                     
                if player1.ans_player1 =="paper" and player1.ans_player2=="sesores":
                    GameServer.objects.filter(pk=id).update(player2Win =  player1.player2Win+1)
                     


                     



                        
          
          
          
    if request.session['Player'] == "Player2":
          if cnt.cnt==0:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )

                GameServer.objects.filter(pk=id).update(ans_player1="" )
                GameServer.objects.filter(pk=id).update(ans_player2=value )
                
                GameServer.objects.filter(pk=id).update(cnt=1 )

                 

                
                GameServer.objects.filter(pk=id).update(player2_click=1 )
                player1 = GameServer.objects.get(id=id)
                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )

                        


          if cnt.cnt==1:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )

                GameServer.objects.filter(pk=id).update(ans_player2=value )
                GameServer.objects.filter(pk=id).update(cnt=0 )

                
                GameServer.objects.filter(pk=id).update(player2_click=1 )
                player1 = GameServer.objects.get(id=id)
                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )


# ------------------- score update 
                if player1.ans_player2 =="paper" and player1.ans_player1=="stone":
                    GameServer.objects.filter(pk=id).update(player2Win =  player1.player2Win+1)
                     
                     
                if player1.ans_player2 =="paper" and player1.ans_player1=="sesores":
                    GameServer.objects.filter(pk=id).update(player1Win =  player1.player1Win+1)
                     



                     


    return redirect(GamePage)









#---------------------------------------------------------------------------------------------------------------------------------- 
def GamePage_sender_sesores(request,value,id):
    cnt = GameServer.objects.get(id=id)

    
     


    if request.session['Player'] == "Player1":
          if cnt.cnt==0:
                
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )



                GameServer.objects.filter(pk=id).update(ans_player2="" )
                GameServer.objects.filter(pk=id).update(ans_player1=value )

                GameServer.objects.filter(pk=id).update(cnt=1 )

                player1 = GameServer.objects.get(id=id)
                GameServer.objects.filter(pk=id).update(player1_click= 1 )

                

                

                 
                

                if player1.player1_click ==1 and player1.player1_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )

                        
                      



                
                

          if cnt.cnt==1:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )



                GameServer.objects.filter(pk=id).update(ans_player1=value )
                GameServer.objects.filter(pk=id).update(cnt=0 )

                GameServer.objects.filter(pk=id).update(player1_click=1 )


                player1 = GameServer.objects.get(id=id)


                

                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )

                        
          

# ------------------- score update 
                if player1.ans_player1 =="sesores" and player1.ans_player2=="paper":
                    GameServer.objects.filter(pk=id).update(player1Win =  player1.player1Win+1)
                  

                if player1.ans_player1 =="sesores" and player1.ans_player2=="stone":
                    GameServer.objects.filter(pk=id).update(player2Win =  player1.player2Win+1)
                     


                     




          
    if request.session['Player'] == "Player2":
          if cnt.cnt==0:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )

                GameServer.objects.filter(pk=id).update(ans_player1="" )
                GameServer.objects.filter(pk=id).update(ans_player2=value )
                
                GameServer.objects.filter(pk=id).update(cnt=1 )

                 

                
                GameServer.objects.filter(pk=id).update(player2_click=1 )
                player1 = GameServer.objects.get(id=id)
                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )

                        


          if cnt.cnt==1:
                num = GameServer.objects.get(id=id)
                #print(f"player 1 id : {num.change}")
                num1=num.change+1
                #print(f"player 1 id : {num1}")
                GameServer.objects.filter(pk=id).update(change= num1 )

                GameServer.objects.filter(pk=id).update(ans_player2=value )
                GameServer.objects.filter(pk=id).update(cnt=0 )

                
                GameServer.objects.filter(pk=id).update(player2_click=1 )
                player1 = GameServer.objects.get(id=id)
                if player1.player1_click ==1 and player1.player2_click ==1 :
                    GameServer.objects.filter(pk=id).update(player1_click=0 )
                    GameServer.objects.filter(pk=id).update(player2_click=0 )



          


          

# ------------------- score update 
                if player1.ans_player2 =="sesores" and player1.ans_player1=="paper":
                    GameServer.objects.filter(pk=id).update(player2Win =  player1.player2Win+1)
                  

                if player1.ans_player2 =="sesores" and player1.ans_player1=="stone":
                    GameServer.objects.filter(pk=id).update(player1Win =  player1.player1Win+1)
                     


                     


                           


                     


    return redirect(GamePage)









#---------------------------------------------------------------------------------------------------------------------------------- 
def GamePage_delete(request,id):

    #num = GameServer.objects.get(id=id)
    #num1=num.change+1
    #GameServer.objects.filter(pk=id).update(change= num1 )
            

    #obj_delete= GameServer.objects.get(id=id)

    GameServer.objects.filter(pk=id).update(status="end" )

    #obj_delete.delete()

    
    num = User.objects.get(id=request.session['Other_Player_Id'])
    num1=num.change+1
    #GameServer.objects.filter(pk=id).update(change= num1 )
    User.objects.filter(pk=request.session['Other_Player_Id']).update(change =  num1)


    request.session['GameServerId'] =''
    request.session['Player'] =''
    request.session['Other_Player_Id'] =''

      
    return redirect(Login)




def GamePage_delete2(request,id):


    #obj_delete= GameServer.objects.get(id=id)   
    #obj_delete.delete()

    request.session['GameServerId'] =''
    request.session['Player'] =''
    request.session['Other_Player_Id'] =''
    
    obj_delete= GameServer.objects.get(id=id)

    #GameServer.objects.filter(pk=id).update(status="end" )

    obj_delete.delete()
      
    return redirect(Login)






def score_2(game_id, update_data):
    GameServer.objects.filter(pk=game_id).update(player2Win=update_data )

    return redirect(GamePage)










#---------------------------------------------------------------------------------------------------------------------------------- 
def Emoji(request,value,id):

    if request.session['Player'] == "Player1":
        num = GameServer.objects.get(id=id)
        num1=num.change+1
        GameServer.objects.filter(pk=id).update(change= num1 )
            
        GameServer.objects.filter(pk=id).update(emoji=value )
         


    if request.session['Player'] == "Player2":
        num = GameServer.objects.get(id=id)
        num1=num.change+1
        GameServer.objects.filter(pk=id).update(change= num1 )
            

        GameServer.objects.filter(pk=id).update(emoji2=value )
                    

    return redirect(GamePage)




def FinalRedirect(request):

   

    return redirect(Login)








def Emoji_User(request,value,id):

    num = User.objects.get(id=request.session['LoginID'])
    num1=num.change+1
    User.objects.filter(pk=request.session['LoginID']).update(change= num1 )
            

    User.objects.filter(pk=request.session['LoginID']).update(emoji=value )

   

    return redirect(Login)



 




def LogOut(request):
    # Retrieve the GameServer object based on player1 field
    try:
        obj_delete = GameServer.objects.get(player1=request.session['LoginID'])
        obj_delete.delete()
    except GameServer.DoesNotExist:
        # Handle the case where the GameServer object does not exist
        pass

    # Clear the LoginID from the session
    

    # Update the status of the User object to "offline"
    
    User.objects.filter(pk=request.session['LoginID']).update(status="offline")


 # Make sure to import your User model

# Assuming your User model has a field named 'change'
    User.objects.update(change=randint(0, 10000)) 

    request.session['LoginID'] = ''
    
    # Redirect to the Home view after logout
    #messages.success(request, 'You have been successfully logged out.')
    return redirect(Home)


















