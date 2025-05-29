import csv
import yaml
import os

class Metrica:
    def __init__(self, id_metrica, archivo_config):
        self.id_metrica = id_metrica
        self.archivo_config = archivo_config
        self.mediciones = []
        self.datos = []
        self.datos_filtrados = []
        self.intervalo = None
        self.puntos_minuto = None
        self.csv_entrada = None
        self.csv_salida = None

        self.leer_config()
        self.leer_datos()
        self.filtrar_datos()

    def leer_config(self):
        with open(self.archivo_config, 'r') as f:
            config = yaml.safe_load(f)
        self.csv_entrada = config['entrada']['archivo_datos']
        self.csv_salida = config['salida']['nombre_archivo']
        self.puntos_minuto = config['salida']['puntos_minuto']

    def leer_datos(self):
        with open(self.csv_entrada, newline='') as f:
            reader = csv.DictReader(f)
            self.datos = []
            for row in reader:
                # Convertir campos numéricos
                dato = {}
                for k, v in row.items():
                    if k == 'timestamp':
                        dato[k] = int(v)
                    else:
                        try:
                            dato[k] = float(v)
                        except ValueError:
                            dato[k] = v
                self.datos.append(dato)
        # Forward fill para valores faltantes
        keys = self.datos[0].keys() if self.datos else []
        for k in keys:
            last_val = None
            for d in self.datos:
                if d[k] == '' or d[k] is None:
                    d[k] = last_val
                else:
                    last_val = d[k]

    def obtener_intervalo(self):
        return int(60 / self.puntos_minuto)

    def filtrar_datos(self):
        self.intervalo = self.obtener_intervalo()
        if not self.datos:
            self.datos_filtrados = []
            return

        indices = [0]
        ultimo = self.datos[0]['timestamp']
        for i in range(1, len(self.datos)):
            actual = self.datos[i]['timestamp']
            if actual - ultimo >= self.intervalo:
                indices.append(i)
                ultimo = actual
        self.datos_filtrados = [self.datos[i] for i in indices]

    def procesar_datos(self):
        raise NotImplementedError("Implementar en subclase")

    def guardar_csv(self):
        columnas = ['timestamp', 'id_metrica', 'numero_medida', 'valor']
        with open(self.csv_salida, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            for fila in self.mediciones:
                writer.writerow(fila)
        print(f"Guardado en {self.csv_salida}")

    


class MetricaCalorHumedo(Metrica):
    def __init__(self, archivo_config):
        super().__init__(12, archivo_config)

    def procesar_datos(self):
        self.mediciones = []
        for i, d in enumerate(self.datos_filtrados):
            temps = d.get('temperatura', 0)
            hums = d.get('humedad', 0)
            valor = temps + 0.1 * hums
            self.mediciones.append([d['timestamp'], self.id_metrica, i + 1, valor])


class MetricaRuidoCorregido(Metrica):
    def __init__(self, archivo_config):
        super().__init__(31, archivo_config)

    def procesar_datos(self):
        self.mediciones = []
        for i, d in enumerate(self.datos_filtrados):
            ruidos = d.get('ruido', 0)
            presiones = d.get('presion', 0)
            valor = ruidos - 0.05 * (presiones - 1013)
            self.mediciones.append([d['timestamp'], self.id_metrica, i + 1, valor])


class MetricaAlertaAmbiental(Metrica):
    def __init__(self, archivo_config):
        super().__init__(87, archivo_config)

    def procesar_datos(self):
        self.mediciones = []
        for i, d in enumerate(self.datos_filtrados):
            temps = d.get('temperatura', 0)
            hums = d.get('humedad', 0)
            ruidos = d.get('ruido', 0)
            alerta = 0
            if temps > 35 or hums < 20 or ruidos > 90:
                alerta = 1
            self.mediciones.append([d['timestamp'], self.id_metrica, i + 1, alerta])
