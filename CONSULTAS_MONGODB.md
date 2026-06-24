# Consultas MongoDB Principales

Este archivo contiene las consultas principales usadas en el proyecto, con comentarios breves para explicar que hace cada una.


```javascript
// Busca todos los eventos.
// El segundo parametro indica que campos se mostraran.
db.eventos.find(
  {},
  {
    _id: 0,
    codigo: 1,
    nombre: 1,
    fecha: 1,
    lugar: 1,
    categoria: 1
  }
)
```

## 1. Buscar invitados por nombre

```javascript
// Busca invitados cuyo nombre contenga la palabra ingresada.
// $regex permite buscar por coincidencia parcial.
// $options: "i" ignora mayusculas y minusculas.
db.invitados.find(
  {
    nombre: {
      $regex: "ana",
      $options: "i"
    }
  },
  {
    _id: 0,
    rut: 1,
    nombre: 1,
    correo: 1,
    empresa: 1,
    estado: 1
  }
)
```

## 2. Buscar invitados por dominio de correo

```javascript
// Busca invitados cuyo correo contenga el dominio indicado.
// Ejemplos: empresa.cl, inacap.cl, contratista.cl
db.invitados.find(
  {
    correo: {
      $regex: "empresa.cl",
      $options: "i"
    }
  },
  {
    _id: 0,
    rut: 1,
    nombre: 1,
    correo: 1,
    empresa: 1,
    estado: 1
  }
)
```


```javascript
// Busca eventos donde el arreglo invitados tenga un invitado con ese RUT.
db.eventos.find(
  {
    "invitados.rut": "11.019.752-6"
  }
)
```

## 3. Buscar si un invitado esta confirmado en un evento

```javascript
// Busca un evento especifico y valida que dentro del arreglo invitados
// exista el RUT indicado con estado confirmado.
db.eventos.findOne(
  {
    codigo: "EVT-2025-001",
    invitados: {
      $elemMatch: {
        rut: "11.019.752-6",
        estado: "confirmado"
      }
    }
  }
)
```

## 4. Top 3 eventos con mas invitados confirmados

```javascript
// $unwind separa el arreglo invitados para trabajar invitado por invitado.
// $match filtra solo invitados confirmados.
// $group agrupa por evento y cuenta confirmados con $sum.
// $sort ordena de mayor a menor.
// $limit deja solo los primeros 3 resultados.
db.eventos.aggregate([
  {
    $unwind: "$invitados"
  },
  {
    $match: {
      "invitados.estado": "confirmado"
    }
  },
  {
    $group: {
      _id: {
        codigo: "$codigo",
        nombre: "$nombre"
      },
      total_confirmados: {
        $sum: 1
      }
    }
  },
  {
    $sort: {
      total_confirmados: -1
    }
  },
  {
    $limit: 3
  }
])
```

## 5. Invitados confirmados de un evento con datos personales

```javascript
// $match busca el evento por codigo.
// $unwind separa los invitados del evento.
// $match deja solo los confirmados.
// $lookup une con la coleccion invitados usando el RUT.
// $project define los campos que se mostraran al final.
db.eventos.aggregate([
  {
    $match: {
      codigo: "EVT-2025-001"
    }
  },
  {
    $unwind: "$invitados"
  },
  {
    $match: {
      "invitados.estado": "confirmado"
    }
  },
  {
    $lookup: {
      from: "invitados",
      localField: "invitados.rut",
      foreignField: "rut",
      as: "datos_invitado"
    }
  },
  {
    $unwind: "$datos_invitado"
  },
  {
    $project: {
      _id: 0,
      codigo: 1,
      evento: "$nombre",
      rut: "$datos_invitado.rut",
      nombre: "$datos_invitado.nombre",
      correo: "$datos_invitado.correo",
      empresa: "$datos_invitado.empresa",
      estado_invitado: "$datos_invitado.estado",
      estado_evento: "$invitados.estado"
    }
  }
])
```

