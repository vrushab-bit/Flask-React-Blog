import React from 'react'
import axios from "axios";

import Navbar from './../components/Navbar'
import MediaCard from './../components/Card'


const Home = () => {

  const [post, setPost] = React.useState(null);

  React.useEffect(() => {
    axios.get('http://127.0.0.1:5000/').then((response) => {
      setPost(response.data);
    });
  }, []);

  console.log(post);

  return (
    <div>
      <Navbar/>

      <MediaCard title="Hello World" description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et aliquet massa. Duis tincidunt tincidunt leo et finibus. Sed lacinia malesuada turpis, ac feugiat nunc ultrices at. Nulla facilisi. Ut tincidunt quam imperdiet ante luctus volutpat. Maecenas purus urna, dapibus sit amet lobortis vitae, imperdiet lacinia ex."/>
      
    </div>
  
  )
}

export default Home