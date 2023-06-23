import {useEffect, useState} from 'react'

import { useHistory } from "react-router-dom";

const Home = () => {


    return ( 
        <div className='homeAll'>
            <div className='HomeLink'>
                <a  className='link' href='/player'>Player</a>
                <a  className='link' href='/socket'>Socket</a>
            </div>
        </div>
     );
}
 
export default Home;