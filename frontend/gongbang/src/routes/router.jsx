import React from "react";
import { Route, Routes } from "react-router-dom";
import Main from "../pages/Main";
import CoffeeCafe from "../pages/CoffeeCafe";
import StudyCafe from "../pages/StudyCafe";
import CafeDetail from "../pages/CafeDetail";
import Signup from "../pages/Accounts/Signup";
import Login from "../pages/Accounts/Login";
import ReviewCreate from "../pages/ReviewCreate";
import ReviewUpdate from "../pages/ReviewUpdate";
import CoffeCafeCreate from "../pages/CoffeCafeCreate";
import Review from "../pages/Reveiw";
import ReviewU from "../pages/ReviewU";


export default function Router() {
    return (
        <>
            <Routes>
                <Route path="/" element={<Main />}/>
                <Route path="/coffeecafe" element={<CoffeeCafe />}/>
                <Route path="/coffeecafe/:id" element={<CafeDetail />}/>
                <Route path="/coffeecafe/:id/review" element={<ReviewCreate />}/>
                <Route path="/review/:id" element={<ReviewU />}/>
                <Route path="/studycafe" element={<StudyCafe />}/>
                <Route path="/login" element={<Login />}/>
                <Route path="/signup" element={<Signup />}/>
                <Route path= "/admin/coffeecafe/create" element = {<CoffeCafeCreate/>}/>
                <Route path= "coffeecafe/:id/review/all" element={<Review/>}/>
            </Routes>
        </>
    );
}