<template>
    <v-dialog max-width="500px">
        <template v-slot:activator="{props: activatorProps}">
            <v-btn v-bind="activatorProps">Add Stream</v-btn>
        </template>
         <template v-slot:default="{ isActive }">
            <v-card title="Create a new stream:">
                <v-form v-model="valid" validate-on="submit" @submit.prevent="submit">
                    <v-radio-group v-model="form_stream_type">
                        <v-radio v-for="type in stream_types"
                        :label="type" :value="type"></v-radio>
                    </v-radio-group>
                    <v-container v-if="form_stream_type == 'UDP'">
                        <v-text-field
                        v-model="form_stream_name"
                        :rules="name_rules"
                        label="Stream name:"
                        required>
                        </v-text-field>

                        <v-text-field
                        v-model="form_stream_ip"
                        :rules="ip_rules"
                        label="Stream IP:"
                        required>
                        </v-text-field>

                        <v-text-field
                        v-model="form_stream_port"
                        :rules="port_rules"
                        label="Stream port:"
                        required>
                        </v-text-field>

                        <v-text-field
                        v-model="form_stream_buffer"
                        :rules="buffer_rules"
                        label="Stream buffer size:"
                        required>
                        </v-text-field>
                    </v-container>
                    <v-btn
                    v-model="btn_val"
                    text="submit"
                    type="submit"
                    block></v-btn>
                </v-form>        
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                    text="Close Dialog"
                    @click="isActive.value = false"
                    ></v-btn>
                </v-card-actions>
            </v-card>
         </template>
    </v-dialog>
    <v-alert class="alert_sty" v-model="alerting" :type="alert_type" closable>
        {{ alert_msg }}
    </v-alert>
</template>

<script setup>
    import axios from 'axios';
    import { onBeforeMount, ref } from 'vue';
    const valid = ref(false)
    const form_stream_name = ref('')
    const form_stream_type = ref('UDP')
    const form_stream_ip = ref('')
    const form_stream_port = ref('')
    const form_stream_buffer = ref('1024')
    const stream_types = ['UDP']  // Should make a getter on the backend 
    const alerting = ref(false)
    const alert_type = ref('success')
    const alert_msg = ref('success')
    const btn_val = true

    const name_rules = [
        inp => {
            if (inp) return true
            return 'this is a mandatory field.'
        }
    ]

    const ip_rules = [
        inp => {
            if (inp) return true
            return 'this is a mandatory field.'
        },
        inp => {
            if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(inp)) {
                return true
            }
            else {
                return 'Invalid IP :('
            }
        }]

    const port_rules = [
        inp => {
            if (inp) return true
            return 'this is a mandatory field.'
        },
        inp => {
            if (Number.isInteger(Number(inp))) {
                return true
            }
            else {
                return 'Please enter an integer between 0 and 65,535.'
            }
        },
        inp => {
            if (inp >= 0 && inp <= 65535) {
                return true
            }
            else {
                return 'Please enter an integer between 0 and 65,535.'
            }
        }
    ]

    const buffer_rules = [
        inp => {
            if (inp) return true
            return 'this is a mandatory field.'
        },
        inp => {
            if (Number.isInteger(Number(inp))) {
                return true
            }
            else {
                return 'Please enter an integer.'
            }
        }
    ]

    async function submit(form_data) {
        if (!valid.value) return
        const response = await axios.post('http://127.0.0.1:8000/stream_manager/create/udp',
            {
                'name': form_stream_name.value,
                'ip': form_stream_ip.value,
                'port': form_stream_port.value,
                'recv_buffer': form_stream_buffer.value,
                'parsers': []
            }
        ).then((response) => {
            console.log(response)
            if (response.status == 200) {
                alert_type.value = 'success'
                alert_msg.value = 'success'
                alerting.value = true
            } 
        }).catch((response) => {
            alert_type.value = 'error'
            alert_msg.value = response.response.data.detail
            alerting.value = true
        }).finally((response) => {
            // setTimeout(() => {
            //     alerting.value = false
            // }, 2000)
        })
    }
</script>

<style>
    .alert_sty {
        position: fixed;
        bottom: 0;
    }
</style>