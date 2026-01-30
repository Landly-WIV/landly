import flet as ft
import backend.logRegAuth as au
import re

def inpVal(e, regStr):
    if re.match(regStr, e.control.value):
        e.control.border_color = ft.Colors.GREEN
        e.control.error = None
    elif e.control.value == "":
        e.control.border_color = ft.Colors.GREY_400
        e.control.error = None
    else:
        e.control.border_color = ft.Colors.ORANGE
        e.control.error = None
    e.control.update()

def bluVal(e, regStr):
    if e.control.value != "" and not re.match(regStr, e.control.value):
        e.control.error = "Ungültige Eingabe"
        e.control.border_color = ft.Colors.RED
    elif re.match(regStr, e.control.value):
        e.control.error = None
        e.control.border_color = ft.Colors.GREEN
    else:
        e.control.error = None
        e.control.border_color = ft.Colors.GREY_400
    e.control.update()

def sub(e, fie, page):
    if fie[0]:
        if fie[6].value and fie[7].value:
            if not fie[6].error and not fie[7].error:
                if fie[9].value:
                    fie[8].value = f"Login erfolgreich für: {fie[6].value}"
                    fie[8].color = ft.Colors.GREEN
                    au.setLog(fie[6].value)
                    au.updVie(page)
                else:
                    fie[8].value = "Bitte Accountart angeben!"
                    fie[8].color = ft.Colors.RED
            else:
                fie[8].value = "Bitte alle Felder korrekt ausfüllen!"
                fie[8].color = ft.Colors.RED
        else:
            fie[8].value = "Bitte alle Felder ausfüllen!"
            fie[8].color = ft.Colors.RED
    else:
        if fie[6].value and fie[4].value and fie[7].value:
            if not fie[6].error and not fie[4].error and not fie[7].error:
                if fie[9].value:
                    if fie[7].value == fie[5].value:
                        fie[8].value = f"Registrierung erfolgreich für: {fie[6].value}"
                        fie[8].color = ft.Colors.GREEN
                        au.setLog(fie[6].value)
                        au.updVie(page)
                    else:
                        fie[8].value = "Passwörter stimmen nicht überein!"
                        fie[8].color = ft.Colors.RED
                else:
                    fie[8].value = "Bitte Accountart angeben!"
                    fie[8].color = ft.Colors.RED
            else:
                fie[8].value = "Bitte alle Felder korrekt ausfüllen!"
                fie[8].color = ft.Colors.RED
        else:
            fie[8].value = "Bitte alle Felder korrekt ausfüllen!"
            fie[8].color = ft.Colors.RED
    
    page.update()

def swiMod(e, fie, page):
    fie[0] = not fie[0]
    
    if fie[0]:
        fie[1].value = "Anmelden"
        fie[2].text = "Anmelden"
        fie[3].text = "Noch kein Konto? Registrieren"
        fie[4].visible = False
        fie[5].visible = False
    else:
        fie[1].value = "Registrieren"
        fie[2].text = "Registrieren"
        fie[3].text = "Bereits ein Konto? Anmelden"
        fie[4].visible = True
        fie[5].visible = True
    
    fie[6].value = ""
    fie[4].value = ""
    fie[7].value = ""
    fie[5].value = ""
    fie[8].value = ""
    fie[9].value = None
    
    page.update()

def logRegPag(page):
    log = True

    useReg = r"^[a-zA-Z0-9]{2,}$"
    emaReg = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    pasReg = r"^[a-zA-Z0-9?!_-]{8,16}$"
    
    useFie = ft.TextField(
        label="Benutzername",
        width=300,
        prefix_icon=ft.Icons.PERSON,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-Z0-9]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, useReg),
        on_blur=lambda e: bluVal(e, useReg)
    )
    
    emaBut = ft.TextField(
        label="E-Mail",
        width=300,
        prefix_icon=ft.Icons.EMAIL,
        visible=False,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-Z0-9._%+-@]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, emaReg),
        on_blur=lambda e: bluVal(e, emaReg)
    )
    
    pasFie = ft.TextField(
        label="Passwort",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-Z0-9?!_-]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, pasReg),
        on_blur=lambda e: bluVal(e, pasReg)
    )
    
    pasConFie = ft.TextField(
        label="Passwort bestätigen",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        visible=False,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-Z0-9?!_-]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, pasReg),
        on_blur=lambda e: bluVal(e, pasReg)
    )

    radGro = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="bauer", label="Bauer"),
                ft.Radio(value="kunde", label="Kunde"),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    mesTex = ft.Text(value="", color=ft.Colors.RED, size=14)
    
    titTex = ft.Text(
        value="Anmelden",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN
    )
    
    subBut = ft.ElevatedButton(
        content="Anmelden",
        width=300,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.BLACK,
        on_click=lambda e: sub(e, fie, page)
    )
    
    togBut = ft.TextButton(
        content="Noch kein Konto? Registrieren",
        on_click=lambda e: swiMod(e, fie, page)
    )

    fie = [
        log, 
        titTex, 
        subBut, 
        togBut, 
        emaBut, 
        pasConFie, 
        useFie, 
        pasFie, 
        mesTex,
        radGro
    ]
    
    logRegCol = ft.Column(
        controls=[
            ft.Row(height=50),
            titTex,
            ft.Row(height=20),
            useFie,
            emaBut,
            pasFie,
            pasConFie,
            radGro,
            ft.Row(height=10),
            mesTex,
            ft.Row(height=10),
            subBut,
            togBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )
    
    return logRegCol