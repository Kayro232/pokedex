import flet as ft
import aiohttp
import winsound


poke_actual = 0
#reproductor con pygame

#sonido de incio de la app
winsound.PlaySound('C:/Windows/Media/notify.wav',winsound.SND_FILENAME)

async def main(page:ft.page):
   page.title = "pokedex"
   page.theme_mode= "dark"
   page.window_width = 430
   page.window_height = 650
   page.window_resizable = False
   page.window_horizontal = "center"
   page.window_vertical = "center"
   audio1 = ft.Audio(
        src="https://www.cjoint.com/doc/24_05/NEreL0c5enL_pokemon-palet.mp3", autoplay=True
    )
   page.overlay.append(audio1.play())
   page.update()
   
   #definiendo poke
   texto= ft.Text(value="")
   #haciendo las funciones
   async def peticion(url):
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
            return await response.json()
         
   async def evento_vacio(e):
     global poke_actual
     incremento = 1 if e.control == flechasuperior else -1
     poke_actual = (poke_actual - 1 + incremento) % 1000 + 1
     
     resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{poke_actual}")
     datos = f"Number:{poke_actual}\nName: {resultado['name']}\n\nAbilities:"
     for elemento in resultado['abilities']:
            
            habilidad = elemento['ability']['name']
            datos += f"\n{habilidad}"
     datos += f"\n\nHeight: {resultado['height']}"
     texto.value= datos
      
     items_tercero[1] = ft.Container(ft.Text(value=f"{datos}",text_align="center"),width=250,bgcolor=ft.colors.GREEN,border_radius=20,height=233)
     sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{poke_actual}.png"
     imagenes.src = sprite
     page.update()


   
   sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
   #poniendo las imagenes
   imagenes =  ft.Image(
                src= sprite,
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
               )
           
   
   #creando los items pra el primero
   luz_azul =  ft.Container(width=100,height=100,shape=ft.BoxShape.CIRCLE,bgcolor=ft.colors.BLUE)
   items = [
      luz_azul,
      ft.Container(width=30,height=30,bgcolor=ft.colors.YELLOW),
      ft.Container(width=30,height=30,bgcolor=ft.colors.PINK_100),
      ft.Container(width=30,height=30,bgcolor=ft.colors.PINK_700),
   ]
   #creando la pantalla donde se van a ver los pokemones 
   items_segundo = ft.Container(imagenes,width=300,height=300,border=ft.border.all(),bgcolor=ft.colors.WHITE)
   #creando el triagulo para los botones
   triangulo = ft.canvas.Canvas([
      ft.canvas.Path([
         ft.canvas.Path.MoveTo(40,0),
         ft.canvas.Path.LineTo(0,50),
         ft.canvas.Path.LineTo(80,50),
      ],
      paint= ft.Paint(
            style= ft.PaintingStyle.FILL,
       ),
      ),
   ],
   width= 50,
   height= 50
   )
   flechasuperior=ft.Container(triangulo,width=80,height=50,on_click=evento_vacio)
   #creando los botones
   flechas = ft.Column(spacing=9,controls=[
      flechasuperior,
      ft.Container(triangulo,rotate=ft.Rotate(angle=3.14159),width=80,height=50,on_click=evento_vacio),
   ])
   #creando los botenes dentro del tercer container
   items_tercero = [
      ft.Container(width=30),
      ft.Container(content=ft.Text(value=f""),padding=100,width=250,bgcolor=ft.colors.GREEN,border_radius=20,),
      ft.Container(width=80,height=120,content=flechas,),
      ft.Container(width=30),
   ]

   #creando los contenedores
   primero = ft.Container(content=ft.Row(items),width=500,height=50,alignment=ft.alignment.center)

   segundo =  ft.Container(content=items_segundo,width=420,height=250,alignment=ft.alignment.center,bgcolor=ft.colors.BLACK)

   tercero =  ft.Container(content=ft.Row(items_tercero),width=420,height=250,alignment=ft.alignment.center)

   cum = ft.Column(controls=[
      primero,
      segundo,
      tercero
   ])

   page.add(cum)
ft.app(target=main)