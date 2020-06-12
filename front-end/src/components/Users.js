import React, { useState } from "react";
const API = process.env.REACT_APP_API;

export const Users = () => {
  const [name, setName] = useState("");
  const [user, setUser] = useState({});

  //object to retrieve errors -----> delete once db is ready
  const dataError = {
    Nombres: "Not Found",
    Genero: "Not Found",
    Pais: "Not Found",
    image:
      "https://lightwidget.com/wp-content/uploads/2018/05/local-file-not-found-295x300.png",
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API}${name}`);
      const data = await res.json();
      setUser(data);
    } catch {
      setUser(dataError);
    }
  };

  return (
    <>
      <div className="row">
        <div className="col-md-2"></div>
        <div className="col-md-8">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <input
                type="text"
                onChange={(e) => setName(e.target.value)}
                value={name}
                className="form-control"
                placeholder="Type a Name to know it's gender"
                autoFocus
              />
            </div>
            <button className="btn btn-primary btn-block"> Search </button>
          </form>
        </div>
        <div className="col-md-2"></div>
      </div>
      <div className="col-md-12 p-4">
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Nombres</th>
              <th>Genero</th>
              <th>Pais de origen</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{user.Nombres}</td>
              <td>{user.Genero}</td>
              <td>{user.Pais}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        className="container"
        style={{ justifyContent: "center", display: "flex" }}
      >
        <h2>{user.name}</h2>
      </div>
      <div
        className="container"
        style={{ justifyContent: "center", display: "flex" }}
      ></div>
    </>
  );
};
