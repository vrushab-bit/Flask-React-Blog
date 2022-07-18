import React from 'react'
import './Navbar.css'

const Navbar = () => {
  return (
    <div>
        <nav class="navbar">
          <div class="container">

             <div class="navbar-header">
                <a href="#">
                  <h4>Blog App</h4>
                </a>
             </div>

              <div class="navbar-menu" id="open-navbar1">
                 <ul class="navbar-nav">
                   <li class="active"><a href="/">Post List</a></li>
                  <li><a href="/add">Add Post</a></li>

                  </ul>
               </div>
          </div>
        </nav>
    </div>
  )
}

export default Navbar