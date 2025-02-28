# NeuralTherapist

## Pokročilý BCI systém pro terapeutické aplikace | Advanced BCI System for Therapeutic Applications

### 🇨🇿 Česky

#### Popis projektu
NeuralTherapist je pokročilý webový systém mozek-počítač (BCI) určený pro terapeutické aplikace. Systém umožňuje komplexní analýzu mozkových signálů a ovládání robotických asistentů přímo z webového prohlížeče.

#### Klíčové funkce
- Real-time vizualizace BCI signálů pomocí Plotly.js
- Interaktivní webové rozhraní pro ovládání systému
- Bezpečnostní monitoring a nouzové zastavení
- Uživatelský průvodce pro nové uživatele
- Interaktivní nápověda pro komplexní BCI prvky
- Vícejazyčné rozhraní (čeština)

#### Systémové požadavky
- Python 3.11 nebo vyšší
- Flask framework
- Webový prohlížeč s podporou JavaScript
- Sériový port pro BCI zařízení
- Sériový port pro robotického asistenta

#### Instalace
1. Naklonujte repozitář:
```bash
git clone https://github.com/zbynekcz12/NeuralTherapist.git
cd NeuralTherapist
```

2. Nainstalujte potřebné závislosti:
```bash
pip install -r requirements.txt
```

3. Nastavte konfiguraci v `src/config.py`:
- BCI_SERIAL_PORT: Port BCI zařízení
- ROBOT_SERIAL_PORT: Port robotického asistenta
- Další parametry podle potřeby

#### Spuštění aplikace
1. Spusťte hlavní aplikaci:
```bash
python src/main.py
```

2. Otevřete webový prohlížeč na adrese:
```
http://localhost:5000
```

#### Bezpečnostní upozornění
- Před použitím systému se ujistěte, že máte správně nastavené nouzové zastavení
- Pravidelně kontrolujte připojení BCI zařízení a robotického asistenta
- Dodržujte bezpečnostní protokoly pro práci s BCI zařízeními

### 🇬🇧 English

#### Project Description
NeuralTherapist is an advanced brain-computer interface (BCI) web system designed for therapeutic applications. The system enables complex brain signal analysis and control of robotic assistants directly from a web browser.

#### Key Features
- Real-time BCI signal visualization using Plotly.js
- Interactive web interface for system control
- Safety monitoring and emergency stop
- User guide for new users
- Interactive tooltips for complex BCI elements
- Multilingual interface (Czech)

#### System Requirements
- Python 3.11 or higher
- Flask framework
- Web browser with JavaScript support
- Serial port for BCI device
- Serial port for robotic assistant

#### Installation
1. Clone the repository:
```bash
git clone https://github.com/zbynekcz12/NeuralTherapist.git
cd NeuralTherapist
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure settings in `src/config.py`:
- BCI_SERIAL_PORT: BCI device port
- ROBOT_SERIAL_PORT: Robotic assistant port
- Other parameters as needed

#### Running the Application
1. Start the main application:
```bash
python src/main.py
```

2. Open web browser at:
```
http://localhost:5000
```

#### Safety Warnings
- Ensure emergency stop is properly configured before using the system
- Regularly check BCI device and robotic assistant connections
- Follow safety protocols for working with BCI devices

### 📄 License | Licence
MIT License

Copyright (c) 2025 NeuralTherapist