import React, {SyntheticEvent, useState} from 'react';
import {Redirect} from 'react-router-dom';

const Register = () => {

    
    const [name, setName] = useState('');
    const [username, setUsername] = useState('');
    const [UserPhonenumber, setUserPhonenumber] = useState('');
   // const [PhotoFileName, setPhoto] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [redirect, setRedirect] = useState(false);
    const [PhotoFileName, setPhoto] = useState<File | null>(null);
    const [childName, setchildName] = useState('');
    const [childAge, setchildAge] = useState('');
    const [isChildDepressed, setisChildDepressed] = useState('');
    const [isChildBullied, setisChildBullied] = useState('');
    const [describeYourChildBehaviour, setdescribeYourChildBehaviour] = useState('');
    const handleImageUpload = (evt: React.ChangeEvent<HTMLInputElement>) => {
        if (evt.target.files != null) {
          setPhoto(evt.target.files[0]); //error
        }
      };
    
    const submit = async (e: SyntheticEvent) => {
        e.preventDefault();
        var data = new FormData();
        data.append('name', name);
        data.append('email', email);
        data.append('password', password);
        data.append('username', username);
        data.append('childName', childName);
        data.append('childAge', childAge);
        data.append('isChildDepressed', isChildDepressed);
        data.append('isChildBullied', isChildBullied);
        data.append('describeYourChildBehaviour', describeYourChildBehaviour);
        data.append('UserPhonenumber', UserPhonenumber);
        data.append('PhotoFileName', PhotoFileName as Blob);
        console.log(data)
        await fetch('http://localhost:8000/api/register', {
            mode: 'no-cors',
            method: "POST",
            body: data
        }).then(function (res) {
            if (res.ok) {
              alert("Perfect! ");
            } else if (res.status === 401) {
              alert("Oops! ");
            }
          }, function (e) {
            alert("Error submitting form!");
          });

        setRedirect(true);
    }

    if (redirect) {
        return <Redirect to="/login"/>;
    }

    return (
        <form encType="multipart/form-data" action="" onSubmit={submit}>
            <h1 className="h3 mb-3 fw-normal">Please register</h1>
            <label htmlFor='idName'>Name: </label>
            <input id="idName" className="form-control" placeholder="Name" required
                   onChange={e => setName(e.target.value)}
            />
            <label htmlFor='idEmail'>Email: </label>
            <input id="idEmail" type="email" className="form-control" placeholder="Email Address" required
                   onChange={e => setEmail(e.target.value)}
            />
            <label htmlFor='idPwd'>Password: </label>
            <input id="idPwd" type="password" className="form-control" placeholder="Password" required
                   onChange={e => setPassword(e.target.value)}
            />
            <label htmlFor='idUsername'>Username: </label>
            <input id="idUsername" className="form-control" placeholder="Username" required
                   onChange={e => setUsername(e.target.value)}
            />
            <label htmlFor='idChildName'>What's the name of your child: </label>
            <input id="idChildName" className="form-control" placeholder="Child Name" required
                   onChange={e => setchildName(e.target.value)}
            />
            <label htmlFor='idChildAge'>How old is your child: </label>
            <input id="idChildAge" className="form-control" placeholder="Child Age" required
                   onChange={e => setchildAge(e.target.value)}
            />
            <label htmlFor='idisChildDepressed'>Does your child suffers from depression? </label>
            <input id="idisChildDepressed" className="form-control" placeholder="Child's History with Depression" required
                   onChange={e => setisChildDepressed(e.target.value)}
            />
            <label htmlFor='idisChildBullied'>Did your child experienced bullying? </label>
            <input id="idisChildBullied" className="form-control" placeholder="Child's History with Bullying" required
                   onChange={e => setisChildBullied(e.target.value)}
            />
            <label htmlFor='iddescribeYourChildBehaviour'>Describe your child's behavioral issues: </label>
            <input id="iddescribeYourChildBehaviour" className="form-control" placeholder="Child's Behavioral Issues" required
                   onChange={e => setdescribeYourChildBehaviour(e.target.value)}
            />
            <label htmlFor='idPhoneNumber'>Phone Number: </label>
            <input id="idPhoneNumber" className="form-control" placeholder="Phone Number" required
                   onChange={e => setUserPhonenumber(e.target.value)}
            />
            <label htmlFor='idPhoto'>Upload Your Photo: </label>
       <input id="idPhoto" type="file" onChange={handleImageUpload}/>
            
            <button className="w-100 btn btn-lg btn-primary" type="submit">Submit</button>
        </form>
    );
};

export default Register;
