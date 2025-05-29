# %%
import unittest
import os
import yaml
import pandas as pd
from Metrica2 import MetricaCalorHumedo, MetricaRuidoCorregido, MetricaAlertaAmbiental

class TestMetricasBasico(unittest.TestCase):

    def crear_archivos(self):
        config = {
            'entrada': {
                'archivo_datos': 'test_input.csv'
            },
            'salida': {
                'puntos_minuto': 6,
                'nombre_archivo': 'test_output.csv'
            }
        }
        with open('test_config.yaml', 'w') as f:
            yaml.dump(config, f)

        # Armando csv para testear
        csv_data = """timestamp,temperatura,humedad,ruido,presion
1000,25,50,60,1010
1005,26,55,62,1011
1010,27,60,58,1012
1015,28,65,61,1013
1020,29,70,65,1014
1025,30,75,70,1015
"""
        with open('test_input.csv', 'w') as f:
            f.write(csv_data)

    def borrar_archivos(self):
        # Borrar archivos de prueba si existen
        if os.path.exists('test_config.yaml'):
            os.remove('test_config.yaml')
        if os.path.exists('test_input.csv'):
            os.remove('test_input.csv')
        if os.path.exists('test_output.csv'):
            os.remove('test_output.csv')

    def test_calor_humedo(self):
        # Preparar archivos
        self.crear_archivos()

        # Crear instancia y procesar datos
        met = MetricaCalorHumedo('test_config.yaml')
        met.procesar_datos()

        # Verificar que la cantidad de mediciones es igual a filas filtradas
        self.assertEqual(len(met.mediciones), len(met.df_filtrado))

        # Verificar que el primer valor calculado es el esperado (temperatura + 0.1*humedad)
        valor_esperado = 25 + 0.1 * 50
        self.assertEqual(met.mediciones[0][3], valor_esperado)

        # Borrar archivos después de la prueba
        self.borrar_archivos()

    def test_ruido_corregido(self):
        self.crear_archivos()

        met = MetricaRuidoCorregido('test_config.yaml')
        met.procesar_datos()

        self.assertEqual(len(met.mediciones), len(met.df_filtrado))
        valor_esperado = 60 - 0.05 * (1010 - 1013)
        self.assertEqual(met.mediciones[0][3], valor_esperado)

        self.borrar_archivos()

    def test_alerta_ambiental(self):
        self.crear_archivos()

        met = MetricaAlertaAmbiental('test_config.yaml')
        met.procesar_datos()

        # Primer registro no debería activar alerta (valor 0)
        self.assertEqual(met.mediciones[0][3], 0)

        # Modificar temperatura para forzar alerta y procesar de nuevo
        met.df_filtrado.at[0, 'temperatura'] = 40
        met.procesar_datos()

        # Ahora debería ser alerta 1
        self.assertEqual(met.mediciones[0][3], 1)

        self.borrar_archivos()

    def test_guardar_csv(self):
        self.crear_archivos()

        met = MetricaCalorHumedo('test_config.yaml')
        met.procesar_datos()
        met.guardar_csv()

        # Verificar que el archivo de salida fue creado
        self.assertTrue(os.path.exists(met.csv_salida))

        # Leer archivo y verificar columnas
        df = pd.read_csv(met.csv_salida)
        self.assertEqual(list(df.columns), ['timestamp', 'id_metrica', 'numero_medida', 'valor'])

        # Verificar que el número de filas es correcto
        self.assertEqual(len(df), len(met.mediciones))

        self.borrar_archivos()


if __name__ == '__main__':
    unittest.main()


