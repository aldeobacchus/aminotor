import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Test from './containers/Test/Test';
import Game from './containers/Game/Game';
import Home from './containers/Home/Home';
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, createRoutesFromElements, RouterProvider, Route } from "react-router-dom";
import { createRoot } from "react-dom/client";
import ErrorView from './containers/ErrorView';

const router = createBrowserRouter(
  createRoutesFromElements(
      <Route errorElement={<ErrorView />}>
        <Route path="/" element={<App />}></Route>
      </Route>
  )
);

createRoot(document.getElementById("root")!).render(
  <RouterProvider router={router} />
);



// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
