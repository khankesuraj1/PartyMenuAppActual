import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MenuScreen from "./components/MenuScreen";
import IngredientScreen from "./components/IngredientScreen";

function App() {
  return (
    <div className="App min-h-screen bg-gray-50">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MenuScreen />} />
          <Route path="/ingredients/:dishId" element={<IngredientScreen />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;