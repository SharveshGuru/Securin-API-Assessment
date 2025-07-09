import {useState, useEffect} from "react";
import axios from "axios";

const RecipieTable=()=>{
    const [recipies,setRecipies]=useState([]);
    const [total,setTotal]=useState(0);
    const [page,setPage]=useState(1);
    const [detailsToggle, setDetailsToggle]=useState(false);
    const [details,setDetails]=useState();
    const fetchRecipies=async(page)=>{
        const response = await axios.get(`http://localhost:8000/api/recipies?page=${page}`);
        setRecipies(response.data.data);
        setTotal(response.data.total);
    }

    useEffect(()=>{
        fetchRecipies(page);
    },[page]);

    function toggleDetails(recipie){
        setDetailsToggle(!detailsToggle);
        setDetails(recipie);
    }

    return(
        <div style={{margin:"1rem"}}>
            <h1>Recipies List</h1>
            <div style={{margin:"1rem"}}>
                <button onClick={()=>setPage((p)=>Math.max(p-1,1))} disabled={page===1}>Previous</button>
                <span>Page {page} of {total}</span>
                <button onClick={()=>setPage((p)=>Math.min(p+1,total))} disabled={page===total}>Next</button>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Cusine</th>
                        <th>Rating</th>
                        <th>Total Time</th>
                        <th>No. of People serves</th>
                        <th>View Details</th>
                    </tr>
                </thead>
                <tbody>
                    {recipies.map((recipie)=>(
                        <tr key={recipie.id}>
                            <td>{recipie.title}</td>
                            <td>{recipie.cuisine}</td>
                            <td>{recipie.rating}</td>
                            <td>{recipie.total_time}</td>
                            <td>{recipie.serves}</td>
                            <td>{detailsToggle?<button onClick={()=>toggleDetails(recipie)}>Hide</button>:<button onClick={()=>toggleDetails(recipie)}>Show</button>}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* {detailsToggle && <div style={{margin:"1rem"}}>
                <h1>{details.title}</h1>
                <h1>{details.}</h1>
                </div>} */}
        </div>
    )
}
export default RecipieTable;