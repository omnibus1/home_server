import {useEffect, useState} from 'react'

import { useHistory } from "react-router-dom";
import config from "./Config.json"
const Player = () => {
    const link=config["IP_ADDRESS"]

    const [avilableSongs,setAvilableSongs]=useState([])
    const [songQueue,setSongQueue]=useState([])
    const [update,setUpdate]=useState(false)

    useEffect(()=>{
        fetch(link+"/avilable_songs")
        .then(res=>{
            return res.json()
        })
        .then((data)=>{
            setAvilableSongs(data['avilable_songs'])
            
        })
    },[])

    useEffect(()=>{
        fetch(link+"/song_queue")
        .then(res=>{
            return res.json()
        })
        .then((data)=>{
            setSongQueue(data['queue'])
            console.log(data['queue'])
            
        })
    },[update])

    const handleAddSong=async(e)=>{
        let song_name=e.target.getAttribute('data-value')
        const request_body={song_name}
        console.log(JSON.stringify(request_body))
        fetch(link+'/play_song',{
            method: "POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify(request_body)},
        ).then(()=>{
            console.log("added song")
            setUpdate(!update)
        })
    }

    return ( 
        <div className='playerAll'>
            <div className='queueAll'>
                <h1 className='queueText'>Current Queue:</h1>
                {songQueue.map((song)=>
                    <div>{song}</div>
                )}
            </div>
            <h1>Avilable songs:</h1>
            <div className='avilableSongs'>
                {avilableSongs.map((song)=>
                    <div className='song' >
                        <p className='songName'>{song}</p>
                        <li className='playButton' data-value={song} onClick={(e)=>handleAddSong(e)}>ADD</li>
                    </div>
                )}

            </div>


        </div>
     );
}
 
export default Player;