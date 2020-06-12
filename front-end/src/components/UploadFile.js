import React, { Component } from "react";
import axios from "axios";

export class UploadFile extends Component {
  state = {
    title: "",
    content: "",
    file: null,
  };

  handleChange = (e) => {
    this.setState({
      [e.target.id]: e.target.value,
    });
  };

  handeFileChange = (e) => {
    this.setState({
      file: e.target.files[0],
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    console.log(this.state);
    const form_data = new FormData();
    form_data.append("file", this.state.file, this.state.file.name);
    form_data.append("title", this.state.title);
    form_data.append("content", this.state.content);
    const url = "http://localhost:8000/api/posts/";
    axios
      .post(url, form_data, {
        headers: {
          "content-type": "multipart/form-data",
        },
      })
      .then((res) => {
        // console.log(res.data);
      })
      .catch((err) => console.log(err));
  };

  render() {
    return (
      <>
        <div
          style={{
            boxShadow:
              "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
            height: "270px",
            borderRadius: "8px",
          }}
          className="col-md-8"
        >
          <form onSubmit={this.handleSubmit}>
            <div
              className="card-header"
              style={{ background: "none", textAlign: "center" }}
            >
              Upload a .xlsx, .csv or a .json file
            </div>
            <p>
              <input
                className="form-control"
                type="text"
                placeholder="Title"
                id="title"
                value={this.state.title}
                onChange={this.handleChange}
                required
              />
            </p>
            <p>
              <input
                className="form-control"
                type="text"
                placeholder="Description"
                id="content"
                value={this.state.content}
                onChange={this.handleChange}
                required
              />
            </p>
            <p>
              <input
                className="btn btn-secondary btn-block"
                type="file"
                id="file"
                onChange={this.handeFileChange}
                required
              />
            </p>
            <input
              style={{ height: "40px" }}
              className="btn btn-primary btn-block"
              type="submit"
            />
          </form>
        </div>
      </>
    );
  }
}
