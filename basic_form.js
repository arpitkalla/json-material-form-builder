const [name, setName] = useState('');
const [age, setAge] = useState('');
const [sex, setSex] = useState('Male');
const [phone_number, setPhoneNumber] = useState('');
const [email, setEmail] = useState('');
const onSubmit = () => {
    console.log({
        "name": name,
        "age": age,
        "sex": sex,
        "phone_number": phone_number,
        "email": email,
    });
}
return (
    <FormControl>
        <div class="row-0">
            <TextField id="standard-basic" label="Name" onChange={e => setName(e.target.value)} />
        </div>
        <div class="row-1">
            <TextField id="standard-basic" label="Age" onChange={e => setAge(e.target.value)} />
        </div>
        <div class="row-2">
            <FormLabel component="legend">Sex</FormLabel>
            <RadioGroup aria-label="sex" name="sex" onChange={e => setSex(e.target.value)} value={sex}>
                <FormControlLabel value="Male" control={<Radio />} label="Male" />
                <FormControlLabel value="Female" control={<Radio />} label="Female" />
            </RadioGroup>
        </div>
        <div class="row-3">
            <TextField id="standard-basic" label="Phone No" onChange={e => setPhoneNumber(e.target.value)} />
            <TextField id="standard-basic" label="Email" onChange={e => setEmail(e.target.value)} />
        </div>
        <Button color="primary" onClick={onSubmit}>Submit</Button>
    </FormControl>
)