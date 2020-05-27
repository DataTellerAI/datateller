import React from 'react'

export const About = () => (
    <>
        <h1>About</h1>
        <p> 
            En la mayoría de registros para aplicaciones, servicios, suscripciones etc, normalmente se solicita el nombre, correo y un password. Ahora bien si ya tienes una base de datos, y quieres conocer el género de tus usuarios para facilitar la segmentación y perfilamiento, nuestra api ofrece el servicio de identificar el género según el nombre para cumplir tus objetivos tanto comerciales como académicos.
        </p>
        <p>
            Nuestra api usará un algoritmo de clasificación y un modelo de machine learning que ha sido entrenado con nombres tradicionalmente usados en personas de habla hispana para arrojar el género que se le atribuye comúnmente al nombre consultado. No se puede determinar a través de la api ninguna otra característica demográfica (Edad, nivel socioeconómico, etc) que se pueda llegar a inferir a través del nombre.
        </p>
    </>
)