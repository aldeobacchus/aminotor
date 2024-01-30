import React from 'react';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, createRoutesFromElements, RouterProvider, Route } from "react-router-dom";
import { createRoot } from "react-dom/client";
import ErrorView from './containers/ErrorView';
import Test from './containers/Test/Test'

const router = createBrowserRouter(
  createRoutesFromElements(
      <Route errorElement={<ErrorView />}>
        <Route path="/" element={<App />}></Route>
        <Route path="/test" element={<Test />}></Route>
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