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
        if fie[4].value and fie[6].value:
            if not fie[4].error and not fie[6].error:
                if fie[8].value:
                    sucVal = au.logUse(fie[4].value, fie[6].value)
                    if sucVal:
                        fie[7].value = f"Login erfolgreich für: {fie[4].value}"
                        fie[7].color = ft.Colors.GREEN
                        page.update()
                        au.updVie(page)
                    else:
                        fie[7].value = "Email oder Passwort falsch!"
                        fie[7].color = ft.Colors.RED
                else:
                    fie[7].value = "Bitte Accountart angeben!"
                    fie[7].color = ft.Colors.RED
            else:
                fie[7].value = "Bitte alle Felder korrekt ausfüllen!"
                fie[7].color = ft.Colors.RED
        else:
            fie[7].value = "Bitte alle Felder ausfüllen!"
            fie[7].color = ft.Colors.RED
    else:
        if fie[8].value == "bauer":
            if fie[4].value and fie[6].value and fie[9].value and fie[10].value:
                if not fie[4].error and not fie[6].error and not fie[9].error and not fie[10].error:
                    if fie[6].value == fie[5].value:
                        sucVal = au.regUse(fie[4].value, fie[6].value, fie[8].value, firNam=fie[9].value, konPer=fie[10].value)
                        if sucVal:
                            fie[7].value = f"Registrierung erfolgreich für: {fie[4].value}"
                            fie[7].color = ft.Colors.GREEN
                            page.update()
                            au.updVie(page)
                        else:
                            fie[7].value = "Email bereits registriert!"
                            fie[7].color = ft.Colors.RED
                    else:
                        fie[7].value = "Passwörter stimmen nicht überein!"
                        fie[7].color = ft.Colors.RED
                else:
                    fie[7].value = "Bitte alle Felder korrekt ausfüllen!"
                    fie[7].color = ft.Colors.RED
            else:
                fie[7].value = "Bitte alle Felder ausfüllen!"
                fie[7].color = ft.Colors.RED
        elif fie[8].value == "kunde":
            if fie[4].value and fie[6].value and fie[11].value and fie[12].value:
                if not fie[4].error and not fie[6].error and not fie[11].error and not fie[12].error:
                    if fie[6].value == fie[5].value:
                        sucVal = au.regUse(fie[4].value, fie[6].value, fie[8].value, vorNam=fie[11].value, nacNam=fie[12].value)
                        if sucVal:
                            fie[7].value = f"Registrierung erfolgreich für: {fie[4].value}"
                            fie[7].color = ft.Colors.GREEN
                            page.update()
                            au.updVie(page)
                        else:
                            fie[7].value = "Email bereits registriert!"
                            fie[7].color = ft.Colors.RED
                    else:
                        fie[7].value = "Passwörter stimmen nicht überein!"
                        fie[7].color = ft.Colors.RED
                else:
                    fie[7].value = "Bitte alle Felder korrekt ausfüllen!"
                    fie[7].color = ft.Colors.RED
            else:
                fie[7].value = "Bitte alle Felder ausfüllen!"
                fie[7].color = ft.Colors.RED
        else:
            fie[7].value = "Bitte Accountart angeben!"
            fie[7].color = ft.Colors.RED
    
    page.update()

def swiMod(e, fie, page):
    fie[0] = not fie[0]
    
    if fie[0]:
        fie[1].value = "Anmelden"
        fie[2].content = ft.Text("Anmelden")
        fie[3].content = ft.Text("Noch kein Konto? Registrieren")
        fie[5].visible = False
        fie[4].visible = True
        fie[9].visible = False
        fie[10].visible = False
        fie[11].visible = False
        fie[12].visible = False
    else:
        fie[1].value = "Registrieren"
        fie[2].content = ft.Text("Registrieren")
        fie[3].content = ft.Text("Bereits ein Konto? Anmelden")
        fie[4].visible = True
        fie[5].visible = True
        updRolFie(fie, page)
    
    fie[4].value = ""
    fie[6].value = ""
    fie[5].value = ""
    fie[7].value = ""
    fie[8].value = None
    fie[9].value = ""
    fie[10].value = ""
    fie[11].value = ""
    fie[12].value = ""
    
    page.update()

def updRolFie(fie, page):
    if fie[8].value == "bauer":
        fie[9].visible = True
        fie[10].visible = True
        fie[11].visible = False
        fie[12].visible = False
    elif fie[8].value == "kunde":
        fie[9].visible = False
        fie[10].visible = False
        fie[11].visible = True
        fie[12].visible = True
    else:
        fie[9].visible = False
        fie[10].visible = False
        fie[11].visible = False
        fie[12].visible = False
    page.update()

def logRegPag(page):
    log = True

    emaReg = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    pasReg = r"^[a-zA-Z0-9?!_-]{8,16}$"
    namReg = r"^[a-zA-ZäöüÄÖÜß\s]{2,}$"
    
    emaBut = ft.TextField(
        label="E-Mail",
        width=300,
        prefix_icon=ft.Icons.EMAIL,
        visible=True,
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

    firNamFie = ft.TextField(
        label="Firmenname",
        width=300,
        prefix_icon=ft.Icons.BUSINESS,
        visible=False,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-ZäöüÄÖÜß\s]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, namReg),
        on_blur=lambda e: bluVal(e, namReg)
    )

    konPerFie = ft.TextField(
        label="Kontaktperson",
        width=300,
        prefix_icon=ft.Icons.PERSON,
        visible=False,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-ZäöüÄÖÜß\s]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, namReg),
        on_blur=lambda e: bluVal(e, namReg)
    )

    vorNamFie = ft.TextField(
        label="Vorname",
        width=300,
        prefix_icon=ft.Icons.PERSON,
        visible=False,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-ZäöüÄÖÜß\s]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, namReg),
        on_blur=lambda e: bluVal(e, namReg)
    )

    nacNamFie = ft.TextField(
        label="Nachname",
        width=300,
        prefix_icon=ft.Icons.PERSON,
        visible=False,
        input_filter=ft.InputFilter(
            regex_string=r"^[a-zA-ZäöüÄÖÜß\s]*$",
            allow=True
        ),
        error=None,
        border_color = ft.Colors.GREY_400,
        on_change=lambda e: inpVal(e, namReg),
        on_blur=lambda e: bluVal(e, namReg)
    )

    fie = []

    radGro = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="bauer", label="Bauer"),
                ft.Radio(value="kunde", label="Kunde"),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        on_change=lambda e: updRolFie(fie, page)
    )
    
    mesTex = ft.Text(value="", color=ft.Colors.RED, size=14)
    
    titTex = ft.Text(
        value="Anmelden",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN
    )
    
    subBut = ft.ElevatedButton(
        content=ft.Text("Anmelden"),
        width=300,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.BLACK,
        on_click=lambda e: sub(e, fie, page)
    )
    
    togBut = ft.TextButton(
        content=ft.Text("Noch kein Konto? Registrieren"),
        on_click=lambda e: swiMod(e, fie, page)
    )

    fie.extend([
        log, 
        titTex, 
        subBut, 
        togBut, 
        emaBut, 
        pasConFie, 
        pasFie, 
        mesTex,
        radGro,
        firNamFie,
        konPerFie,
        vorNamFie,
        nacNamFie
    ])
    
    logRegCol = ft.Column(
        controls=[
            ft.Row(height=20),
            titTex,
            ft.Row(height=20),
            firNamFie,
            konPerFie,
            vorNamFie,
            nacNamFie,
            emaBut,
            pasFie,
            radGro,
            ft.Row(height=10),
            mesTex,
            ft.Row(height=10),
            subBut,
            togBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    return logRegCol
