import React from "react"
import './style.css'
import {Container, Row, Col, Form, FormGroup, Label, Input, Button} from 'reactstrap';
import Header from '../Header'
import './style.css'

export default class DecryptPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }
    render() {
        return (
            <Container fluid={true} className="page">
                <Row>
                    <Col>
                        <Header text={this.props.text}/>
                        <h3>
                            Please, attach encrypted picture and put the key below
                        </h3>
                        <Form>
                            <FormGroup>
                                <Row>
                                    <Col>
                                        <Label for="encryptedImage">Initial image</Label>
                                    </Col>
                                    <Col>
                                        <Input type="file" name="encrypted_image" id="encryptedImage" placeholder="Encrypted image" />
                                    </Col>
                                </Row>
                            </FormGroup>

                            <FormGroup>
                                <Row>
                                    <Col>
                                        <Label for="key">Key</Label>
                                    </Col>
                                    <Col>
                                        <Input type="input" name="key_decrypt" id="key" placeholder="Key for decrypting" />
                                    </Col>
                                </Row>
                            </FormGroup>

                        </Form>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Button color="secondary">Decrypt</Button>
                    </Col>
                </Row>
            </Container>
        );
    }
}