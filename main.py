from metrica import MetricaCalorHumedo
from metrica import MetricaRuidoCorregido
from metrica import MetricaAlertaAmbiental

def correr_todas():
    archivo_config = [
        'config/config_calor_humedo.yaml',
        'config/config_ruido_corregido.yaml',
        'config/config_alerta_ambiental.yaml'
    ]

    metricas = [
        MetricaCalorHumedo("config_calor_humedo.yaml"),
        MetricaRuidoCorregido("config_ruido_corregido.yaml"),
        MetricaAlertaAmbiental("config_alerta_ambiental.yaml")
    ]

    for metrica in metricas:
        metrica.procesar_datos()
        metrica.guardar_csv()

if __name__ == '__main__':
    correr_todas()




