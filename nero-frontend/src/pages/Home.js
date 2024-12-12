import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      <h1>Welcome to NERO</h1>
      <p>
        Manage your tasks efficiently. <Link to="/tasks">Go to Tasks</Link>
      </p>
    </div>
  );
}

export default Home;
