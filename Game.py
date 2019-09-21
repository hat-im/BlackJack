from tkinter import *
from BlackJack import *
import time
class GameWindow:
    def __init__(self, master):
        #initializing objects from logic class
        self.deck=Deck()
        self.player=Player(self.deck)
        self.dealer=Dealer(self.deck)
        self.player_images=[]
        self.dealer_images=[]
        self.backdeck=PhotoImage(file="back-red.gif")

        self.master=master
        master.geometry("800x600")
        master.title("BlackJack")

        #definin the frame where all the widgets are placed
        self.background_canvas=Canvas(master, height=600, width=800, bg="green4")
        self.background_canvas.pack()

        #defining widgets
        self.hit_button=Button(self.background_canvas,compound=CENTER, text="Hit", activeforeground="gold", fg="yellow", image=self.backdeck, bg="green4", command=self.hit, state=DISABLED, font=("System",14))
        self.stand_button=Button(self.background_canvas,text="Stand", fg="yellow", activeforeground="gold", bg="green4", activebackground="green", command=self.stand, state=DISABLED, font=("System", 14))
        self.deal_button=Button(self.background_canvas, text="Deal", fg="white", bg="red1", activebackground="red", command=self.enable_buttons, font=("System", 14))
        self.score_label=Label(self.background_canvas, text="Score: ", fg="red", bg="green", font=("System", 12))
        self.winner_label=Label(self.background_canvas, text="Winner", fg="blue", bg="green")

        #placing the widgets and binding events
        self.hit_button.place(anchor=CENTER, relx=0.5, rely=0.5)
        self.deal_button.place(anchor=CENTER, relx=0.5, rely=0.9, width=200, height=50)
        self.score_label.place(anchor=CENTER, relx=0.5, rely=0.7)

    def enable_buttons(self):
        #enables the hit and stand buttons and removes the deal button from the screen
        self.deal_button.place_forget()
        self.display_cards()
        self.display_cards(False)
        self.hit_button.config(state=NORMAL)
        self.stand_button.config(state=NORMAL)
        self.score_label.config(text="Score: "+str(score(self.player.hand)))
        self.stand_button.place(anchor=CENTER, relx=0.5, rely=0.9, width=100, height=50)
        if self.is_game_over():
            self.game_over()

    def hit(self):
        self.player.hand=self.player.hand+self.deck.deal()
        self.score_label.config(text="Score: "+str(score(self.player.hand)), fg="red", bg="green")
        self.display_card()
        if self.is_game_over():
            self.game_over()

    def stand(self):
        self.dealer_turn()
        if self.is_game_over():
            self.game_over()

    def is_game_over(self):
        if score(self.player.hand)>=21 or score(self.dealer.hand)>=21:
            return True
        else:
            return False
    def game_over(self):
        #removing gameplay buttons
        self.hit_button.place_forget()
        self.stand_button.place_forget()
        self.score_label.place_forget()

        #putting up quit button by repurposing the old deal_button
        self.deal_button.config(text="Quit", command=self.master.quit)
        self.deal_button.place(anchor=CENTER, relx=0.5, rely=0.9, width="400", height=50)
        
        #display winner name
        p_s=score(self.player.hand) #player score
        d_s=score(self.dealer.hand) #dealer score
        if p_s==21 or d_s>21:
            winner_name=0
        elif d_s==21 or p_s>21:
            winner_name=1
        else:
            winner_name=0 if p_s>d_s else 1
        self.winner_label.config(text="You lose\nThe dealer wins" if winner_name==1 else "You win!", font=("System",20))
        self.winner_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    def image_name(self, card):
        return card[1].lower()+str(card[0])+".gif"

    def display_cards(self, player_turn=True):
        #displays the first cards of the player or dealer
        if player_turn:
            self.player_images.extend([PhotoImage(file=self.image_name(card)) for card in self.player.hand])
            img=self.background_canvas.create_image(600, -100, image=self.player_images[0], anchor=CENTER)
            for i in range(200):
                self.background_canvas.move(img, 0, 1)
                self.master.update()
                time.sleep(1/200)
            img=self.background_canvas.create_image(600, -100, image=self.player_images[1], anchor=CENTER)
            for i in range(250):
                self.background_canvas.move(img, 0, 1)
                self.master.update()
                time.sleep(1/250)
        else:
            self.dealer_images.extend([PhotoImage(file=self.image_name(card)) for card in self.dealer.hand])
            img=self.background_canvas.create_image(200, -100, image=self.dealer_images[0], anchor=CENTER)
            for i in range(200):
                self.background_canvas.move(img, 0, 1)
                self.master.update()
                time.sleep(1/200)
            img=self.background_canvas.create_image(200, -100, image=self.backdeck, anchor=CENTER)
            for i in range(250):
                self.background_canvas.move(img, 0, 1)
                self.master.update()
                time.sleep(1/250)
            
        
    def display_card(self, player_turn=True):
        #displays the most recently added card of the player/dealer
        if player_turn:
            self.player_images.append(PhotoImage(file=self.image_name(self.player.hand[-1])))
            img=self.background_canvas.create_image(600, -100, image=self.player_images[-1], anchor=CENTER)
            for i in range(150+50*len(self.player.hand)):
                self.background_canvas.move(img, 0, 1)
                self.master.update()
                time.sleep(1/(150+50*len(self.player.hand)))
        else:    
            self.dealer_images.append(PhotoImage(file=self.image_name(self.dealer.hand[-1])))
            if self.dealer.card_down:
                self.background_canvas.create_image(200, 150, image=self.dealer_images[1], anchor=CENTER)
                self.dealer.card_down=False
            img=self.background_canvas.create_image(200, -100, image=self.dealer_images[-1], anchor=CENTER)
            if score(self.dealer.hand)<=17 or self.dealer.last_card<=1:
                for i in range(150+50*len(self.dealer.hand)):
                    self.background_canvas.move(img, 0, 1)
                    self.master.update()
                    time.sleep(1/(150+50*len(self.dealer.hand)))
                time.sleep(0.5)
            
    def dealer_turn(self):
        #disabling buttons
        self.hit_button.place_forget()
        self.stand_button.place_forget()

        #playing dealer turn until it has crossed a total of 17
        while self.dealer.deal_dealer(self.deck):
            self.display_card(False)
        self.game_over()

root=Tk()
gui=GameWindow(root)
root.mainloop()