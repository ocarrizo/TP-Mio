# %%
from metrica import MetricaCalorHumedo
from metrica import MetricaRuidoCorregido
from metrica import MetricaAlertaAmbiental


metricas = [
    MetricaCalorHumedo("config_calor_humedo.yaml"),
    MetricaRuidoCorregido("config_ruido_corregido.yaml"),
    MetricaAlertaAmbiental("config_alerta_ambiental.yaml")
]

for metrica in metricas:
    metrica.leer_datos()
    resultados = metrica.procesar_datos()
    metrica.guardar_csv(resultados)


# if __name__ == '__main__':
#     correr_todas()


