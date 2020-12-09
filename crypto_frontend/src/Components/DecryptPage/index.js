import React from "react"
import './style.css'
import {
    Container,
    Row,
    Col,
    Form,
    FormGroup,
    Label,
    Input,
    Button,
    CustomInput,
    Toast,
    ToastHeader,
    ToastBody, InputGroup, InputGroupAddon
} from 'reactstrap';
import Header from '../Header'
import './style.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export default class DecryptPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isError: false,
            isOpenRes: true,
            wasSent:false,
            file: '',
            key: ''
        };
        this.fieldChange = this.fieldChange.bind(this);
        this.closeResult = this.closeResult.bind(this);
        this.changeShownStatus = this.changeShownStatus.bind(this);
    }

    changeShownStatus() {
        this.setState({isShown: !this.state.isShown})
    }

    setFieldsToState(e) {
        this.setState({
            [e.target.name]: e.target.value,
            dataChanged: true,
            wasSent:false,
            decodedText: ""
        });
        return new Promise(function (resolve, reject) {
            setTimeout(function () {
                resolve(100);
            }, 200)
        });
    }

    fieldChange(value) {
        this.setFieldsToState(value);
    }

    onSelectFile = e => {

        if (e.target.files && e.target.files.length > 0) {
            this.setState({file_name: e.target.files[0].name});


            const reader = new FileReader();
            reader.addEventListener("load", () =>
                this.setState({file: reader.result})
            );

            reader.readAsDataURL(e.target.files[0]);
        }
    };

    sendDataDecoder() {
        console.log(this.state)

        let options = {
            headers: {
                'Accept': 'application/json',
            },
            method: 'POST'
        };
        options.body = new FormData();
        options.body.append('image', this.state.file)
        // options.body.append('text', this.state.text)
        options.body.append('key', this.state.key)

        this.setState({
            wasSent: true,
            isOpenRes: true
        })
        fetch('/api/decode', options)
            .then((response) => {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' +
                        response.status);
                    this.setState({
                        isError: true
                    });
                    return;
                }
                return response.json();
            })
            .then((data) => {
                console.log(data)
                this.setState({
                    decodedText: data.text,
                    isOpenRes: true,
                    isError: false
                })
            })
            .catch((err) => {
                console.log('Fetch Error:', err);
            });
    }

    closeResult() {
        this.setState({
            isOpenRes: !this.state.isOpenRes
        })
    }

    render() {
        return (
            <Container>

                <Row>
                    <Col>
                        <Header text={this.props.text}/>
                        <h6>If you haven't encrypted your message yet, use out encryptor<Button color={'link'} onClick={()=>{window.location.href = '/encrypt'}}>encryptor</Button></h6>
                        <h4 style={{marginBottom: "32px"}}>
                            Please, attach encrypted picture and put the key below
                        </h4>

                        <Form>
                            <FormGroup>
                                <Row>
                                    <Col sm={12} md={3} lg={2}>
                                        <Label for="encryptedImage">Initial image</Label>
                                    </Col>
                                    <Col>
                                        <CustomInput type="file"
                                                     id="encryptedImage"
                                                     name="file"
                                                     onChange={this.onSelectFile}
                                                     label="Pick a bmp encrypted file!"
                                                     accept={".bmp, .BMP"}/>
                                    </Col>
                                </Row>
                            </FormGroup>

                            <FormGroup>
                                <Row form>
                                    <Col sm={12} md={3} lg={2}>
                                        <Label for="key">Key</Label>
                                    </Col>
                                    <Col>
                                        <InputGroup>
                                            <Input
                                                type="text"
                                                autoComplete="new-password"
                                                name="key"
                                                id="key"
                                                className={this.state.isShown ? "" : "security-key"}
                                                onChange={this.fieldChange}
                                                placeholder="Key for encrypting"/>
                                            <InputGroupAddon addonType="append">
                                                <Button color={this.state.isShown ? "danger" : "secondary"}
                                                        onClick={this.changeShownStatus}>
                                                    <FontAwesomeIcon icon={this.state.isShown ? "eye" : "eye-slash"}/>
                                                </Button>
                                            </InputGroupAddon>
                                        </InputGroup>
                                    </Col>
                                </Row>
                            </FormGroup>

                        </Form>
                    </Col>
                </Row>
                <div className={"center-text"}>
                    <Button
                        size={'lg'}
                        disabled={
                            !(this.state.file.length > 0 &&
                                this.state.key.length > 0)
                        }
                        onClick={() => this.sendDataDecoder()}
                        color="secondary">
                        Decrypt image!
                    </Button>
                </div>

                {this.state.file ?
                    <div>
                        <h2>Decryption preview</h2>
                        <Row>

                            <Col>
                                <h4>Encrypted image</h4>
                                <img id="encryptedFrame" className="rounded mx-auto d-block" src={this.state.file}
                                     alt="Encrypted frame"/>

                            </Col>
                            <Col>
                                {this.state.wasSent ?
                                    <Toast isOpen={this.state.isOpenRes}>
                                        <ToastHeader toggle={this.closeResult}>
                                            Decryption result, be careful
                                        </ToastHeader>
                                        <ToastBody>
                                            {this.state.isError ? <b style={{color: "red"}}>Key is not correct!</b> : this.state.decodedText}
                                        </ToastBody>
                                    </Toast> : <></>}

                            </Col>
                        </Row>
                    </div> : <></>}

            </Container>
        );
    }
}