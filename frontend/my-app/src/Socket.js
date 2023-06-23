import {useEffect, useState} from 'react'
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';



import config from "./Config.json"
const Socket = () => {
    const [socketStatus,setSocketStatus]=useState([])
    const link=config["IP_ADDRESS"]
    const[updated,setUpdated]=useState(false)
    const[runUpdated,setRunUpdated]=useState(false)
    const [runInTheMorning,setRunInTheMorning]=useState([])
    const [loading,setLoading]=useState(false)
    const[jobData,setJobData]=useState([])
    const [duration,setDuration]=useState([])
    useEffect(()=>{
        setLoading(true)
        fetch(link+"/get_socket_status")
        .then(res=>{
            return res.json()
        })
        .then((data)=>{
            setLoading(false)
            setSocketStatus(data["status"].toString())
        })
    },[updated])

    useEffect(()=>{
        fetch(link+"/jobs")
        .then(res=>{
            return res.json()
        })
        .then((data)=>{
            setJobData(data)
            console.log(data)
        })
    },[updated])

    useEffect(()=>{
        
        fetch(link+"/run_status")
        .then(res=>{
            return res.json()
        })
        .then((data)=>{

            setDuration(data["duration"])
            setRunInTheMorning(data["run"])
        })
    },[runUpdated])

    const changeRunConfig=async()=>{
        try {
            let url=""
            if (runInTheMorning==="True")url=link+"/dont_run"
            else url=link+"/do_run"
            console.log(url)
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Error! status: ${response.status}`);
            }

            setRunUpdated(!runUpdated)
            }catch(err) {
                alert("error")
            }
      };



    const handleClick = async (state) => {
        try {
            setLoading(true)
            const response = await fetch(link+state);
          if (!response.ok) {
            throw new Error(`Error! status: ${response.status}`);
          }
          const result = await response.json();
          setUpdated(!updated)
          setLoading(false)
          alert(result["status"])
         } catch (err) {
          alert("error")
        }
      };

      const getColorForJob=(type)=>{
        if(type==="Failed")return "red"
        else if(type==="Succesfull")return "green"
        else if(type==="Not run")return "grey"
        else if(type==="Automatic")return "rgb(39, 90, 255)"
        else if(type==="Manual")return "brown"
      }


      
    return ( 
        <div>    
            <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}open={loading}>
                <CircularProgress color="inherit" />
            </Backdrop>
            <div>
                <h1>{socketStatus}</h1>
                <button onClick={()=>handleClick("/turn_on")} disabled={socketStatus==="Offline"||socketStatus==="On"}>Turn On</button>
                <button onClick={()=>handleClick("/turn_off")} disabled={socketStatus==="Offline"|| socketStatus==="Off"}>Turn Off</button> 
            </div>
            <div>
                <h1>Are we running tomorrow for {duration} minutes?</h1>
                <button onClick={changeRunConfig}>{runInTheMorning}</button>   

            </div>
            <div className='wholeTable'>
                <table className='jobTable'>
                <tr>
                    <th className='tableHeader'>Status</th>
                    <th className='tableHeader'>Duration</th>
                    <th className='tableHeader'>Start Time</th>
                    <th className='tableHeader'>End Time</th>
                    <th className='tableHeader'>Type</th>
                </tr>
                    {jobData.map((job)=>(
                        <tr>
                            <td className='jobTableRow' style={{color: getColorForJob(job["status"])}}>{job["status"]}</td>
                            <td className='jobTableRow'>{job["duration"]}</td>
                            <td className='jobTableRow'>{job["start_time"]}</td>
                            <td className='jobTableRow'>{job["end_time"]}</td>
                            <td className='jobTableRow' style={{color: getColorForJob(job["type"])}} >{job["type"]}</td>
                        </tr>
                    ))}
                </table>
            </div>
        </div>
     );
}
 
export default Socket;