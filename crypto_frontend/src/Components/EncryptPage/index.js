import React from "react"
import './style.css'
import {Container, Row, Col, Form, FormGroup, Label, Input, Button, CustomInput} from 'reactstrap';
import Header from '../Header'
import './style.css'

export default class EncryptPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isError: false
        };
        this.fieldChange = this.fieldChange.bind(this);
    }

    setFieldsToState(e) {
        this.setState({
            [e.target.name]: e.target.value,
            dataChanged: true,
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

    sendDataEncoder() {
        console.log(this.state)

        let options = {
            headers: {
                'Accept': 'application/json',
            },
            method: 'POST'
        };
        options.body = new FormData();
        options.body.append('image', this.state.file)
        options.body.append('text', this.state.text)
        options.body.append('key', this.state.key)


        fetch('/api/encode', options)
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
                    encodedFile: data.image
                })
            })
            .catch((err) => {
                console.log('Fetch Error:', err);
            });
    }


    render() {
        return (
            <Container>
                <Row>
                    <Col>
                        <Header text={this.props.text}/>
                        <h4 style={{marginBottom: "32px"}}>
                            Please, input key, text and attach initial picture (<i>in *.bmp format</i>) below
                        </h4>
                        <Form>
                            <FormGroup>
                                <Row>
                                    <Col sm={12} md={3} lg={2}>
                                        <Label for="initialImage">Initial image</Label>
                                    </Col>
                                    <Col>
                                        <CustomInput type="file"
                                                     id="initialImage"
                                                     name="file"
                                                     onChange={this.onSelectFile}
                                                     label="Pick a bmp file!"
                                                     accept={".bmp, .BMP"}/>
                                    </Col>
                                </Row>
                            </FormGroup>

                            <FormGroup>
                                <Row>
                                    <Col sm={12} md={3} lg={2}>
                                        <Label for="text">Text file</Label>
                                    </Col>
                                    <Col>
                                        <Input type="textarea"
                                               onChange={this.fieldChange}
                                               name="text"
                                               id="text"
                                               placeholder="Text for encrypting"/>
                                    </Col>
                                </Row>
                            </FormGroup>

                            <FormGroup>
                                <Row form>
                                    <Col sm={12} md={3} lg={2}>
                                        <Label for="key">Key</Label>
                                    </Col>
                                    <Col>
                                        <Input type="input"
                                               name="key"
                                               id="key"
                                               onChange={this.fieldChange}
                                            // onClick={()=>{alert('TODO show/hide password')}}
                                               placeholder="Key for encrypting"/>
                                    </Col>
                                </Row>
                            </FormGroup>

                        </Form>
                    </Col>
                </Row>
                <div className={"center-text"}>
                    <Button
                        size={'lg'}
                        onClick={() => this.sendDataEncoder()}
                        color="secondary">
                        Encrypt image!
                    </Button>
                </div>

                {this.state.file ?
                    <div>
                        <h2>Encryption preview</h2>
                        <Row >

                            <Col>
                                <h4>Original image</h4>
                                <img id="originalFrame" className="rounded mx-auto d-block" src={this.state.file}
                                     alt="Original frame"/>

                            </Col>
                            <Col>
                                {this.state.encodedFile ? <div>
                                    <h4>Encrypted image (tap to load)</h4>
                                    <a download="encoded image.bmp" href={this.state.encodedFile} title={"Tap to download file!"}>
                                        <img id="encryptedRes" className="rounded mx-auto d-block"

                                             src={this.state.encodedFile} alt="Encrypted frame"/>
                                    </a>

                                </div> : <></>}
                            </Col>
                        </Row>
                    </div> : <></>}
            </Container>
        );
    }
}