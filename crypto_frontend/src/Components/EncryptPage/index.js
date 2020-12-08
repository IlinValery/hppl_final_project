import React from "react"
import './style.css'
import {Container, Row, Col, Form, FormGroup, Label, Input, Button} from 'reactstrap';
import Header from '../Header'
import './style.css'

export default class EncryptPage extends React.Component {
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
                            Please, attach initial picture, attach the text file,
                            put the key and name the output file below
                        </h3>
                        <Form>
                            <FormGroup>
                                <Row>
                                    <Col>
                                        <Label for="initialImage">Initial image</Label>
                                    </Col>
                                    <Col>
                                        <Input type="file" name="initial_image" id="initialImage" placeholder="Initial image" />
                                    </Col>
                                </Row>
                            </FormGroup>

                            <FormGroup>
                                <Row>
                                    <Col>
                                        <Label for="text">Text file</Label>
                                    </Col>
                                    <Col>
                                        <Input type="file" name="text_file" id="text" placeholder="Text for encrypting" />
                                    </Col>
                                </Row>
                            </FormGroup>

                            <FormGroup>
                                <Row>
                                    <Col>
                                        <Label for="key">Key</Label>
                                    </Col>
                                    <Col>
                                        <Input type="input" name="key_encrypt" id="key" placeholder="Key for encrypting" />
                                    </Col>
                                </Row>
                            </FormGroup>

                        </Form>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Button color="secondary">Encrypt</Button>
                    </Col>
                </Row>
            </Container>
        );
    }
}