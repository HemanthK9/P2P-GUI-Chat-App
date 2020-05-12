#!/usr/bin/env python3
'''Script for Tkinter GUI Chat client'''

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

'''Handles receiving of messages'''
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode('utf8')
            msg_list.insert(tkinter.END, msg)
        '''If client has left the chat'''
        except OSError:
            break

'''Handles sending of messages. In tkinter, if send button is pressed, an event parameter is passed by default'''
def send(event = None):
    '''my_msg is the input field on the GUI, so we extract the message to be sent using msg = my_msg.get()'''
    msg = my_msg.get()
    my_msg.set('')      #Clears input field
    client_socket.send(bytes(msg, 'utf8'))
    if msg == '{quit}':
        client_socket.close()
        top.quit()      '''Close the GUI app'''


'''This function is to be called when the window is closed'''
def on_closing(event = None):
    '''Sets input field to quit, and sends that message'''
    my_msg.set('{quit}')
    send()



if __name__ == '__main__':
    '''Building GUI in main namespace'''
    top = tkinter.Tk()
    top.title('Skidaddle')

    #Frame that holds the list of messages
    '''The Frame widget is very important for the process of grouping and organizing other widgets in a somehow friendly way. It works like a container, which is responsible for arranging the position of other widgets. It uses rectangular areas in the screen to organize the layout and to provide padding of these widgets. A frame can also be used as a foundation class to implement complex widgets.'''
    messages_frame = tkinter.Frame(top)

    '''Variables can also be used to validate the contents of an entry widget, and to change the text in label widgets.'''
    my_msg = tkinter.StringVar()
    '''The set method updates the variable, and notifies all variable observers. You can either pass in a value of the right type, or a string.'''
    my_msg.set('Enter your message here')

    '''To navigate past messages. This widget provides a slide controller that is used to implement vertical scrolled widgets, such as Listbox, Text and Canvas.'''
    scrollbar = tkinter.Scrollbar(messages_frame)

    '''The message list which will be stored in message_frame'''
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50 , yscrollcommand=scrollbar.set)

    '''widget.pack() : This geometry manager organizes widgets in blocks before placing them in the parent widget.
    side argument − Determines which side of the parent widget packs against: TOP (default), BOTTOM, LEFT, or RIGHT.
    fill argument − Determines whether widget fills any extra space allocated to it by the packer, or keeps its own minimal dimensions: NONE (default), X (fill only horizontally), Y (fill only vertically), or BOTH (fill both horizontally and vertically).
    '''
    scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
    msg_list.pack(side = tkinter.RIGHT, fill = tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable = my_msg)
    enrty_field.bind()
