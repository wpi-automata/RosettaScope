<template>
    <v-form v-model="valid" validate-on="submit" @submit.prevent="submit">
        <v-container>
            <v-text-field
            v-model="form_parser_name"
            :rules="name_rules"
            label="Parser name:"
            required>
            </v-text-field>

            <v-select
            v-model="form_parser_stream"
            label="Choose a stream (or multiple)"
            :items="stream_list">
            </v-select>

            <v-text-field
            v-model="form_parser_bind_ip"
            :rules="ip_rules"
            label="Bind IP:"
            required>
            </v-text-field>

            <v-text-field
            v-model="form_parser_bind_port"
            :rules="port_rules"
            label="Bind port:"
            required>
            </v-text-field>

            <v-text-field
            v-model="form_parser_output_ip"
            :rules="ip_rules"
            label="Output IP:"
            required>
            </v-text-field>

            <v-text-field
            v-model="form_parser_output_port"
            :rules="port_rules"
            label="Output port:"
            required>
            </v-text-field>
        </v-container>
        <v-btn
        v-model="btn_val"
        text="submit"
        type="submit"
        block></v-btn>
    </v-form>
</template>

<script setup>
    import axios from 'axios';
    import { onBeforeMount, ref, onMounted} from 'vue';
    const valid = ref(false)
    const form_parser_name = ref('')
    const form_parser_type = ref('')
    const form_parser_stream = ref('')
    const parser_types = ['']  // Should make a getter on the backend 
    const alerting = ref(false)
    const alert_type = ref('success')
    const alert_msg = ref('success')
    const btn_val = true
    const stream_list = ref([])
    const form_parser_bind_ip = ref('')
    const form_parser_bind_port = ref(0)
    const form_parser_output_ip = ref('')
    const form_parser_output_port = ref(0)

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

    async function submit(form_data) {
        if (!valid.value) return
        const response = await axios.post('http://127.0.0.1:8000/parser_manager/create',
            {
                'name': form_parser_name.value,
                'type': 'rovlspoof',
                'streams': [form_parser_stream.value],
                'bind_ip': form_parser_bind_ip.value,
                'bind_port': form_parser_bind_port.value,
                'output_ip': form_parser_output_ip.value,
                'output_port': form_parser_output_port.value
            }
        ).then((response) => {
            console.log(response)
            if (response.status == 200) {
                alert_type.value = 'success'
                alert_msg.value = 'success'
                alerting.value = true
            } 
        }).catch((response) => {
            console.log(response)
            alert_type.value = 'error'
            alert_msg.value = response.response.data.detail
            alerting.value = true
        }).finally((response) => {
            // setTimeout(() => {
            //     alerting.value = false
            // }, 2000)
        })
    }

    async function get_data() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/stream_manager/get_streams');
            console.log(response.data.streams.map(s => s.name))
            return response.data.streams.map(s => s.name)
        }
        catch {
            console.error('data get failed')
        }
        return
    }

    // onMounted(async () => {
    //     stream_list.value = await get_data()
    //     console.log(stream_list.value)
    // })
    onBeforeMount(async () => {
        stream_list.value = await get_data()
        console.log('bingus')
        console.log(stream_list.value)
    })
    // stream_list.value = await get_data()
    // console.log(stream_list.value)
    // console.log('bingus')
</script>