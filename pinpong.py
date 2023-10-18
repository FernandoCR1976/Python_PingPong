import tkinter as tk
import random

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Juego de Ping Pong")

# Configuración de la pantalla
ancho_pantalla = 800
alto_pantalla = 600
canvas = tk.Canvas(ventana, width=ancho_pantalla, height=alto_pantalla, bg="black")
canvas.pack()

# Raqueta
raqueta = canvas.create_rectangle(350, 580, 450, 590, fill="white")

# Pelota
pelota = canvas.create_oval(390,290,410,310, fill='orange')


# Movimiento de la pelota
velocidad_x = random.choice([-2, 2])
velocidad_y = -2

#Contadore para rebotes y marcador
rebotes = 0
marcador = 0

#crear etiqueta para el marcador
marcador_label = canvas.create_text(70,30, text=f"Marcador: {marcador}",fill="white", font=("Arial", 16))

# Función para mover la raqueta
def mover_raqueta(event):
    tecla = event.keysym
    raqueta_pos = canvas.coords(raqueta)

    if tecla == "Left" and raqueta_pos[0] > 0:
        canvas.move(raqueta, -20, 0)
    elif tecla == "Right" and raqueta_pos[2] < ancho_pantalla:
        canvas.move(raqueta, 20, 0)

# Vincular el evento de teclado a la función de mover raqueta
canvas.bind_all("<KeyPress-Left>", mover_raqueta)
canvas.bind_all("<KeyPress-Right>", mover_raqueta)

#Función para reiniciar el juego

def reiniciar_juego():
    global velocidad_x, velocidad_y,pelota, rebotes, marcador

    #Reiniciar la posición de la raqueta y de la pelota
    canvas.coords(raqueta,350, 580, 450, 590)
    
    # Eliminar la pelota existente
    canvas.delete(pelota)

    #volvemos a crear la pelota
    pelota = canvas.create_oval(390, 290, 410, 310,fill="red")

    #Reiniciando la velocidad de la pelota
    velocidad_x = random.choice([-2, 2])
    velocidad_y = -2

    #resetear marcador y rebotes
    rebotes = 0
    marcador = 0
    actualizar_marcador()

    #Quitar el mensaje de game over
    canvas.delete("game_over")

    #Desactivar el Botón de reinicio
    reiniciar_btn.config(state=tk.DISABLED)

    #volvemos a reiniciar el juego
    actualizar_juego()


#Función para actualizar el marcador
def actualizar_marcador():
    canvas.itemconfig(marcador_label, text=f"Marcador: {marcador}")


#Creando Botón de reinicio
reiniciar_btn = tk.Button(ventana, text="Reiniciar Juego", command=reiniciar_juego, state=tk.DISABLED )
reiniciar_btn.pack()


# Bucle principal del juego
def actualizar_juego():
    global velocidad_x, velocidad_y,rebotes,marcador

    
    # Obtener las coordenadas de la pelota
    pelota_pos = canvas.coords(pelota)

    # Rebotar en los bordes
    if pelota_pos[0] <= 0 or pelota_pos[2] >= ancho_pantalla:
        velocidad_x *= -1

    if pelota_pos[1] <= 0:
        velocidad_y *= -1

    # Detectar colisión con la raqueta
    if canvas.coords(raqueta)[0] <= pelota_pos[2] <= canvas.coords(raqueta)[2] and \
            canvas.coords(raqueta)[1] <= pelota_pos[3] <= canvas.coords(raqueta)[3]:
        velocidad_y *= -1

    #Contar los rebotes
    if pelota_pos[3] >= alto_pantalla - 20:
            rebotes +=1
            if rebotes >=5:
                if velocidad_y > 0:
                    velocidad_y += 1
                else:
                    velocidad_y -= 1
                rebotes = 0
            rebotes += 1
            marcador += 1
            actualizar_marcador()
            


    # Game over si la pelota cae fuera de la pantalla
    if pelota_pos[3] >= alto_pantalla:
        canvas.create_text(ancho_pantalla / 2, alto_pantalla / 2, text="Game Over", fill="white", font=("Arial", 24), tags="game_over")
        reiniciar_btn.config(state=tk.NORMAL)
        
    else:
        #Mover la pelota
        canvas.move(pelota, velocidad_x,velocidad_y)
        ventana.after(10, actualizar_juego)
        #Contar los rebotes
        
    

# Iniciar el juego
actualizar_juego()

# Iniciar el bucle de la interfaz
ventana.mainloop()
