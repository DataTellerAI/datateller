import React from "react";

export const UploadFile = () => {
  return (
    <form>
      <div className="col-md-8">
        <label htmlFor="exampleFormControlFile1">
          Upload a file in .xlsx or .csv format
        </label>
        <br></br>
        <img
          className="rounded"
          src="https://www.kindpng.com/picc/m/750-7505563_csv-or-excel-icon-png-download-excel-csv.png"
          alt="Excel"
          style={{ width: "172px", height: "136.6px" }}
        />
        <div className="form-group">
          <input
            type="file"
            className="form-control-file"
            id="exampleFormControlFile1"
            formAction="/"
          />
          <button
            type="submit"
            className="btn btn-primary btn-block"
            formAction="/"
          >
            Upload
          </button>
        </div>
      </div>
    </form>
  );
};
